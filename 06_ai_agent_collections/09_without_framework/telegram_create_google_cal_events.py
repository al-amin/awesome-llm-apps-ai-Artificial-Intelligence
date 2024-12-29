import logging
import pickle
import base64
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, ConversationHandler, filters
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import keyring
import asyncio

# Constants for keyring
SCOPES = ['https://www.googleapis.com/auth/calendar']
KEYRING_SERVICE_NAME = 'google_calendar_api'
KEYRING_CREDENTIALS_KEY = 'credentials'
KEYRING_CLIENT_ID_KEY = 'client_id'
KEYRING_CLIENT_SECRET_KEY = 'client_secret'
KEYRING_CALENDAR_ID_KEY = 'appointments_calendar_id'
KEYRING_TELEGRAM_TOKEN_KEY = 'telegram_token'
KEYRING_CALENDAR_ATTENDEES_EMAIL_ID_KEY = 'appointments_calendar_attendees_email_id'

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Define states for the conversation
SUMMARY, LOCATION, DESCRIPTION, START_TIME, END_TIME = range(5)

def get_client_config():
    """Retrieve the client ID and client secret from the keyring."""
    client_id = keyring.get_password(KEYRING_SERVICE_NAME, KEYRING_CLIENT_ID_KEY)
    client_secret = keyring.get_password(KEYRING_SERVICE_NAME, KEYRING_CLIENT_SECRET_KEY)
    
    if not client_id or not client_secret:
        raise ValueError("Client ID and/or Client Secret not found in keyring. Please run the setup script.")

    return {
        "installed": {
            "client_id": client_id,
            "client_secret": client_secret,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob", "http://localhost"]
        }
    }

def get_telegram_token_and_calendar_id():
    """Retrieve the Telegram token and calendar ID from the keyring."""
    telegram_token = keyring.get_password(KEYRING_SERVICE_NAME, KEYRING_TELEGRAM_TOKEN_KEY)
    calendar_id = keyring.get_password(KEYRING_SERVICE_NAME, KEYRING_CALENDAR_ID_KEY)

    if not telegram_token or not calendar_id:
        raise ValueError("Telegram token and/or Calendar ID not found in keyring. Please run the setup script.")

    return telegram_token, calendar_id

def authenticate_google_calendar():
    """Authenticate and return the Google Calendar API service."""
    creds = None

    # Try to load credentials from keyring
    creds_data = keyring.get_password(KEYRING_SERVICE_NAME, KEYRING_CREDENTIALS_KEY)
    if creds_data:
        creds = pickle.loads(base64.b64decode(creds_data.encode()))

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            client_config = get_client_config()
            flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials to the keyring
        keyring.set_password(KEYRING_SERVICE_NAME, KEYRING_CREDENTIALS_KEY, base64.b64encode(pickle.dumps(creds)).decode())

    return build('calendar', 'v3', credentials=creds)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start the conversation and ask for the event summary."""
    await update.message.reply_text('Welcome to the Google Calendar Bot! Please enter the event summary:')
    return SUMMARY

async def summary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Store the summary and ask for the location."""
    context.user_data['summary'] = update.message.text
    await update.message.reply_text('Enter the location (or type "skip" to leave it blank):')
    return LOCATION

async def location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Store the location and ask for the description."""
    location = update.message.text
    context.user_data['location'] = '' if location.lower() == 'skip' else location
    await update.message.reply_text('Enter the description (or type "skip" to leave it blank):')
    return DESCRIPTION

async def description(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Store the description and ask for the start time."""
    description = update.message.text
    context.user_data['description'] = '' if description.lower() == 'skip' or description == '' else description
    await update.message.reply_text('Enter the start date and time (YYYY-MM-DDTHH:MM:SS) or type "now" for current time:')
    return START_TIME

async def start_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Store the start time and ask for the end time."""
    start_time_input = update.message.text
    if start_time_input.lower() == "now" or start_time_input == "":
        start_time = datetime.utcnow()
    else:
        start_time = datetime.strptime(start_time_input, "%Y-%m-%dT%H:%M:%S")
    context.user_data['start_time'] = start_time.isoformat()

    await update.message.reply_text('Enter the end date and time (YYYY-MM-DDTHH:MM:SS) or type "default" for one hour later:')
    return END_TIME

async def end_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Store the end time and create the event."""
    end_time_input = update.message.text
    if end_time_input.lower() == "default" or end_time_input == "":
        end_time = datetime.fromisoformat(context.user_data['start_time']) + timedelta(hours=1)
    else:
        end_time = datetime.strptime(end_time_input, "%Y-%m-%dT%H:%M:%S")
    context.user_data['end_time'] = end_time.isoformat()

    # Authenticate and create the event
    try:
        service = authenticate_google_calendar()
        telegram_token, calendar_id = get_telegram_token_and_calendar_id()
        event_details = {
            'summary': context.user_data['summary'],
            'location': context.user_data['location'],
            'description': context.user_data['description'],
            'start_time': context.user_data['start_time'],
            'end_time': context.user_data['end_time'],
            'attendees': [{'email': keyring.get_password(KEYRING_SERVICE_NAME, KEYRING_CALENDAR_ATTENDEES_EMAIL_ID_KEY)}]  # Updated email
        }
        created_event = create_event(service, event_details, calendar_id)
        await update.message.reply_text(f"Event '{event_details['summary']}' created successfully! Link: {created_event.get('htmlLink')}")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        await update.message.reply_text("An error occurred while creating the event. Please try again.")

    return ConversationHandler.END

def create_event(service, event_details, calendar_id):
    """Create a Google Calendar event in the specified calendar."""
    event = {
        'summary': event_details['summary'],
        'location': event_details.get('location', ''),
        'description': event_details.get('description', ''),
        'start': {
            'dateTime': event_details['start_time'],
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': event_details['end_time'],
            'timeZone': 'UTC',
        },
        'attendees': event_details.get('attendees', []),
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 60 * 24 * 7},  # 1 week
                {'method': 'email', 'minutes': 60 * 24 * 2},  # 2 days
                {'method': 'email', 'minutes': 60 * 24},      # 1 day
                {'method': 'email', 'minutes': 120},          # 2 hours
            ],
        },
    }
    return service.events().insert(calendarId=calendar_id, body=event).execute()

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel the conversation."""
    await update.message.reply_text('Event creation cancelled.')
    return ConversationHandler.END

def main():
    """Start the bot."""
    # Retrieve the Telegram token and calendar ID from the keyring
    telegram_token, calendar_id = get_telegram_token_and_calendar_id()

    application = ApplicationBuilder().token(telegram_token).build()

    # Define a conversation handler with the states SUMMARY, LOCATION, DESCRIPTION, START_TIME, END_TIME
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            SUMMARY: [MessageHandler(filters.TEXT & ~filters.COMMAND, summary)],
            LOCATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, location)],
            DESCRIPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, description)],
            START_TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, start_time)],
            END_TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, end_time)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    application.add_handler(conv_handler)

    # Use asyncio.run() only if the loop is not already running
    try:
        asyncio.run(application.run_polling())
    except RuntimeError as e:
        if str(e) == "This event loop is already running":
            loop = asyncio.get_event_loop()
            loop.run_until_complete(application.run_polling())
        else:
            raise

if __name__ == '__main__':
    main()

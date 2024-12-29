import pickle
import base64
from datetime import datetime, timedelta
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import keyring

SCOPES = ['https://www.googleapis.com/auth/calendar']
KEYRING_SERVICE_NAME = 'google_calendar_api'
KEYRING_CREDENTIALS_KEY = 'credentials'
KEYRING_CLIENT_ID_KEY = 'client_id'
KEYRING_CLIENT_SECRET_KEY = 'client_secret'

# Use the specific calendar ID for "Appointments"
KEYRING_CALENDAR_ID_KEY = 'appointments_calendar_id'

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
        'attendees': [{'email': attendee.strip()} for attendee in event_details.get('attendees', ['asif.dot.comilla@gmail.com'])],
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

def event_exists(service, event_summary, start_time, calendar_id):
    """Check if an event with the same summary and start time already exists in the specified calendar."""
    try:
        events_result = service.events().list(
            calendarId=calendar_id, timeMin=start_time, singleEvents=True, orderBy='startTime').execute()
        events = events_result.get('items', [])
        for event in events:
            if event['summary'] == event_summary:
                return event
    except Exception as e:
        print(f"An error occurred while checking for existing events: {e}")
    return None

def get_event_details():
    """Get event details from the user."""
    summary = input("Enter event summary: ")
    location = input("Enter location (optional): ")
    description = input("Enter description (optional): ")

    # Prompt for start and end time
    start_time_input = input("Enter start date and time (YYYY-MM-DDTHH:MM:SS) or press Enter for current time: ")
    end_time_input = input("Enter end date and time (YYYY-MM-DDTHH:MM:SS) or press Enter for 10 minutes from now: ")

    # Determine start and end time
    if start_time_input:
        try:
            start_time = datetime.strptime(start_time_input, "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            print("Invalid start date format. Please use YYYY-MM-DDTHH:MM:SS.")
            return None
    else:
        start_time = datetime.utcnow()

    if end_time_input:
        try:
            end_time = datetime.strptime(end_time_input, "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            print("Invalid end date format. Please use YYYY-MM-DDTHH:MM:SS.")
            return None
    else:
        end_time = start_time + timedelta(minutes=10)

    # Convert to ISO 8601 format
    start_time = start_time.isoformat() + 'Z'
    end_time = end_time.isoformat() + 'Z'

    attendees_input = input("Enter attendees emails separated by commas (optional): ")
    attendees = [email.strip() for email in attendees_input.split(',')] if attendees_input else ['asif.dot.comilla@gmail.com']

    return {
        'summary': summary,
        'location': location,
        'description': description,
        'start_time': start_time,
        'end_time': end_time,
        'attendees': attendees
    }

def main():
    try:
        service = authenticate_google_calendar()
        event_details = get_event_details()

        if not event_details:
            return

        # Use the specific calendar ID for "Appointments"
        calendar_id = keyring.get_password(KEYRING_SERVICE_NAME, KEYRING_CALENDAR_ID_KEY)

        # Check if the event already exists in the "Appointments" calendar
        existing_event = event_exists(service, event_details['summary'], event_details['start_time'], calendar_id)
        if existing_event:
            overwrite = input("Event already exists. Do you want to overwrite it? (yes/no): ").strip().lower()
            if overwrite != 'yes':
                print("Event not overwritten.")
                return

        # Create the event in the "Appointments" calendar
        created_event = create_event(service, event_details, calendar_id)
        print(f"Event created in 'Appointments': {created_event.get('htmlLink')}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()

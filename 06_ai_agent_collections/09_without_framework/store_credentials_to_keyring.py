import os
import json
import keyring

KEYRING_SERVICE_NAME = 'google_calendar_api'
KEYRING_CLIENT_ID_KEY = 'client_id'
KEYRING_CLIENT_SECRET_KEY = 'client_secret'
KEYRING_CALENDAR_ID_KEY = 'appointments_calendar_id'
KEYRING_TELEGRAM_TOKEN_KEY = 'telegram_token'

def prompt_for_update(key):
    """Prompt the user to decide whether to update an existing credential."""
    response = input(f"The {key} is already stored. Do you want to update it? (yes/no): ").strip().lower()
    return response == 'yes'

def store_credentials_to_keyring():
    """Load client credentials from the credentials.json file and store them in keyring."""
    if not os.path.exists('credentials.json'):
        raise FileNotFoundError("The credentials.json file is missing.")

    with open('credentials.json', 'r') as file:
        data = json.load(file)

    client_id = data['installed']['client_id']
    client_secret = data['installed']['client_secret']

    # Store client credentials in keyring with confirmation
    if keyring.get_password(KEYRING_SERVICE_NAME, KEYRING_CLIENT_ID_KEY) is None or prompt_for_update('Client ID'):
        keyring.set_password(KEYRING_SERVICE_NAME, KEYRING_CLIENT_ID_KEY, client_id)

    if keyring.get_password(KEYRING_SERVICE_NAME, KEYRING_CLIENT_SECRET_KEY) is None or prompt_for_update('Client Secret'):
        keyring.set_password(KEYRING_SERVICE_NAME, KEYRING_CLIENT_SECRET_KEY, client_secret)

    # Check and store additional information with confirmation
    calendar_id = keyring.get_password(KEYRING_SERVICE_NAME, KEYRING_CALENDAR_ID_KEY)
    if calendar_id is None or prompt_for_update('Appointments Calendar ID'):
        appointments_calendar_id = input("Enter the Appointments Calendar ID: ")
        keyring.set_password(KEYRING_SERVICE_NAME, KEYRING_CALENDAR_ID_KEY, appointments_calendar_id)

    telegram_token = keyring.get_password(KEYRING_SERVICE_NAME, KEYRING_TELEGRAM_TOKEN_KEY)
    if telegram_token is None or prompt_for_update('Telegram Token'):
        telegram_token = input("Enter the Telegram Bot Token: ")
        keyring.set_password(KEYRING_SERVICE_NAME, KEYRING_TELEGRAM_TOKEN_KEY, telegram_token)

    print("Credentials have been processed.")

if __name__ == '__main__':
    store_credentials_to_keyring()

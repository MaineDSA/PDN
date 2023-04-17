# PDN
Sends a community safety alert to subscribers.

## Usage
usage: emergency-alert.py [-m MESAGE]

optional arguments:

  -m, --message MESSAGE

If MESSAGE is not supplied, test message will be sent to AN_TEST_PERSON.
All messages will be appended with opt-out notification, for compliance.

## Environment Variables
- TWILIO_ACCOUNT_SID: Twilio API key/ID
- TWILIO_AUTH_TOKEN: Twilio API authentication token
- TWILIO_FROM_PHONE: Phone number in format 12079111973
- AN_TAG_ID: ID of Action Network tag containing links to people
- AN_API_TOKEN: API Token for Action Network access
- AN_TEST_PERSON: ID of Action Network person to send test message to

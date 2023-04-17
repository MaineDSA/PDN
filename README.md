# PDN
## Usage
```
usage: emergency-alert.py [-h] [-m MESSAGE] [-t]

Sends a community safety alert to subscribers.

options:
  -h, --help                      show this help message and exit
  -m MESSAGE, --message MESSAGE   Specify message to send.
  -t, --test                      Activate test mode to message single recipient.
```
If MESSAGE is not supplied, user will be prompted for message entry.
If not supplied via command line or prompt, test message will be sent to AN_TEST_PERSON.
If AN_TEST_PERSON is not set, user will be prompted for entry of AN API ID for test person.

All messages will be appended with opt-out notification, for compliance.

## Environment Variables
- TWILIO_ACCOUNT_SID: Twilio API key/ID
- TWILIO_AUTH_TOKEN: Twilio API authentication token
- TWILIO_FROM_PHONE: Phone number in format 12079111973
- AN_TAG_ID: ID of Action Network tag containing links to people (will prompt if not found)
- AN_API_TOKEN: API Token for Action Network access
- AN_TEST_PERSON: ID of Action Network person to send test message to (will prompt if not found)

# PDN
## Usage
```
usage: emergency-alert.py [-h] [-r RECIPIENT | -l LIST] [-m MESSAGE]

Sends a community safety alert to subscribers. All messages will be appended with opt-out notification, for compliance.

options:
  -h, --help            show this help message and exit
  -r RECIPIENT, --recipient RECIPIENT   Specify single recipient via Action Network ID.
  -l LIST, --list LIST                  Specify Action Network ID of tag to find recipients in.
  -m MESSAGE, --message MESSAGE         Specify message to send to recipient(s).
```

## Environment Variables
### Authentication
#### Twilio
- TWILIO_ACCOUNT_SID: Twilio API key/ID [REQUIRED]
- TWILIO_AUTH_TOKEN: Twilio API authentication token [REQUIRED]
- TWILIO_FROM_PHONE: Phone number in format 12079111973 [REQUIRED]
#### Action Network
- AN_API_TOKEN: API Token for Action Network access [REQUIRED]
### Configuration
- AN_TAG_ID: ID of Action Network tag containing links to people (will look for command line arg or prompt if not found)
- AN_RECIPIENT_ID: ID of Action Network person to send test message to (will look for command line arg or prompt if not found)
- PDN_MESSAGE: Message to be sent to subscribers (will look for command line arg or prompt if not found)

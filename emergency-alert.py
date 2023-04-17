message = str("Hi $NAME, this is a test of our emergency alert system.")

import os
from twilio.rest import Client
client = Client(os.environ['TWILIO_ACCOUNT_SID'], os.environ['TWILIO_AUTH_TOKEN']) # Use API credentials via environmental variables

from parsons import ActionNetwork
an = ActionNetwork() # Use API credentials via environmental variables

tag = an.get_tag(os.environ['AN_TAG_ID'] + str('/taggings')) # Compile all records tagged in Action Network

def get_person_from_tag(tagging): # Find all people linked in supplied tagging
    if tagging['item_type'] == str('osdi:person'):
        link = str(tagging['_links']['osdi:person']['href'])
        id = link.replace('https://actionnetwork.org/api/v2/people/', '')
        return an.get_person(id)

def get_phone(person):
    for phone in person['phone_numbers']:
        if phone['number_type'] == str('Mobile') and str('number') in phone :
            return phone['number']

def create_message(person):
    given_name = person['given_name'] or ''
    messagetosend = message.replace('$NAME', given_name)
    phone = get_phone(person)
    client.messages.create(
            body = messagetosend,
            from_ = str('+') + os.environ['TWILIO_FROM_PHONE'],
            to = str('+') + phone
        )

def contact_tagged_people(tag):
    for tagging in tag['_embedded']['osdi:taggings']:
        person = get_person_from_tag(tagging)
        create_message(person)

contact_tagged_people(tag)

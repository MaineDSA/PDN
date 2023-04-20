import os
from twilio.rest import Client

# Set up Twilio client with account SID and auth token from environment variables
client = Client(os.environ['TWILIO_ACCOUNT_SID'], os.environ['TWILIO_AUTH_TOKEN'])

import argparse

# Set up argument parser for command-line arguments
parser = argparse.ArgumentParser(description="Sends a community safety alert to subscribers.")
parser.add_argument('-t', '--test', default=False, action="store_true", help="Activate test mode to message single recipient.")
parser.add_argument("-m", "--message", type=str, help="Specify message to send.")

# Parse command-line arguments to check for test mode
testmode = parser.parse_args().test

from parsons import ActionNetwork

# Set up Action Network client
an = ActionNetwork()

def get_phone(person):
    # Iterate through phone numbers and return the mobile number
    for phone in person['phone_numbers']:
        if phone['number_type'] == str('Mobile') and str('number') in phone:
            return phone['number']

def send_message(person, message):
    # Extract the given name from the person object
    given_name = person['given_name'] or ''
    
    # Replace the $NAME placeholder with the person's given name
    messagetosend = message.replace('$NAME', given_name)

    # Get the person's phone number
    phone = get_phone(person)

    if not messagetosend or messagetosend == "": return

    # Send the message using the Twilio client
    client.messages.create(
        body=messagetosend + str(" To opt out, reply \"STOP\"."),
        from_=str('+') + os.environ['TWILIO_FROM_PHONE'],
        to=str('+') + phone
    )

def get_tagged_people(tag):
    # Initialize an empty dictionary to store people
    people = []

    # Iterate through taggings and add people with the specified tag to the dictionary
    for tagging in tag['_embedded']['osdi:taggings']:
        if tagging['item_type'] == str('osdi:person'):
            link = str(tagging['_links']['osdi:person']['href'])
            id = link.replace('https://actionnetwork.org/api/v2/people/', '')
            people.append(an.get_person(id))

    return people

def get_message():
    # Return a test message if in test mode
    if testmode:
        return str("Hi $NAME, this is a test of our emergency alert system.")

    # Get message from command-line arguments or user input
    message = parser.parse_args().message
    if not message:
        message = input("Write a message. $NAME will be replaced with the person's first name. "
                + "Be sure to identify the source of the message. Opt out text will be added automatically to the end. "
                + "To send a test message, don't enter anything. Ctrl+C to cancel. "
            )

    return message

def get_people():
    # Get test person if in test mode
    if testmode:
        testperson_id = os.environ['AN_TEST_PERSON']
        if not testperson_id:
            testperson_id = input("What is the API ID of the Action Network Person to be sent the test message? ")

        return [an.get_person(testperson_id)]

    # Get the tag ID from environment variables or user input
    tagvar = os.environ['AN_TAG_ID']
    if not tagvar:
        tagvar = input("What is the API ID of the Action Network Tag? ")

    if not tagvar:
        testmode = 1
        return get_people()

    # Get the tag object from Action Network
    an_tag = an.get_tag(tagvar + str('/taggings'))

    # Return people with the specified tag
    return get_tagged_people(an_tag)

# Get the message and send it to each person
message = get_message()
people = get_people()
for person in people:
    send_message(person, message)

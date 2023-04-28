import os
from twilio.rest import Client

# Set up Twilio client with account SID and auth token from environment variables
client = Client(os.environ['TWILIO_ACCOUNT_SID'], os.environ['TWILIO_AUTH_TOKEN'])

import argparse

# Set up argument parser for command-line arguments
parser = argparse.ArgumentParser(description="Sends a community safety alert to subscribers. All messages will be appended with opt-out notification, for compliance.")
parser_recipient = parser.add_mutually_exclusive_group()
parser_recipient.add_argument('-r', '--recipient', type=str, help="Specify single recipient via Action Network ID.")
parser_recipient.add_argument("-l", "--list", type=str, help="Specify Action Network ID of tag to find recipients in.")
parser.add_argument("-m", "--message", type=str, help="Specify message to send to recipient(s).")

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
    message = None

    # Get the tag ID from environment variable
    if "PDN_MESSAGE" in os.environ:
        message = os.environ['PDN_MESSAGE']

    # Get the message from command-line argument
    if not message:
        message = parser.parse_args().message

    # Get the message from user input
    if not message:
        message = input("Write a message. $NAME will be replaced with the person's first name. "
                + "Be sure to identify the source of the message. Opt out text will be added automatically to the end. "
                + "Press enter without typing anything to use a test message. Press Ctrl+C to cancel. "
            )

    # Use a test message
    if not message:
        message = str("Hi $NAME, this is a test of our emergency alert system.")

    return message

def get_people():
    tag = None

    # Get the tag ID from environment variable
    if "AN_TAG_ID" in os.environ:
        tag = os.environ['AN_TAG_ID']

    # Get the tag ID from command line argument
    if not tag:
        tag = parser.parse_args().list

    # Get the tag ID from user input
    if not tag:
        tag = input("What is the API ID of the Action Network tag to receive the message? ")

    # Get the tag object from Action Network
    an_tag = an.get_tag(tag + str('/taggings'))

    # Return people with the specified tag
    return get_tagged_people(an_tag)

def get_person():
    recipient = None

    # Get the tag ID from environment variable
    if "AN_RECIPIENT_ID" in os.environ:
        recipient = os.environ['AN_RECIPIENT_ID']

    # Get the tag ID from command line argument
    if not recipient:
        recipient = parser.parse_args().recipient

    # Get the tag ID from user input
    if not recipient and not parser.parse_args().list:
        recipient = input("What is the API ID of the Action Network person to receive the message? Press enter without typing anything to use an Action Network tag ID instead of a person. ")

    # Return the person object from Action Network, if found
    if recipient:
        return [an.get_person(recipient)]

# Get the message and send it to each person
people = get_person() or get_people()
message = get_message()
for person in people:
    send_message(person, message)

'''
These are all of the environment variables we're calling from the PC.
They'll be imported into the other files in this package.

We're using the file so we have one central place from which
to reference them.

If you're installing the talklib module on a PC for the first time, 
make sure all of these are declared in the PC's environment variables.

If you need to change them, you probably want to change them at the PC level, not here.

AUDIO DESTINATIONS:
variable name: destinations
variable value: a comma-separated list of destinations (network or local folders, etc),
for wherever you want the final, processed audio files to end up. You can put a space
after each comma, or not; either way will work.

EMAIL:
variable name: toEmail
variable value: a comma-separated list of email addresses where you want
notifications sent to. You can put a space after each comma, 
or not; either way will work. You need at least one address; there is no
maximum number of addresses. You can ONLY send emails to nashville.gov 
addresses. However, if you send an email to nashvilletalkinglibrary@nashville.gov,
that email will be forwarded to the TL Gmail account, which can then be 
forwarded to any address. Metro ITS set up this relay server for us.

TWILIO
variable name: twilio_to
variable value: a comma-separated list of phone numbers you want alerts/notifications
sent to. This includes both SMS and phone calls. You can put a space after each comma, 
or not; either way will work. You need at least one number; there is no maximum.
The numbers should be formatted like this: +1xxxxxxxxxx with no spaces. That is, 
+1 followed by a ten-digit US phone number. An example variable value: 
+16158625804, +16158625800, +16158501020
'''

import os

class EV:
    def __init__(self):
        self.destinations = sort_destinations() # where should output files go? MUST BE A LIST EVEN WITH ONLY ONE
        self.syslog_host = get_EV(ev="syslog_server") # ip of syslog server (PC with syslog software)
        self.fromEmail = get_EV(ev="fromEmail") # from where should emails appear to come?
        self.toEmail = sort_to_email() # to where should emails be sent?
        self.mail_server = get_EV(ev="mail_server_external")  # IP of mail server (ITS set this up for us)
        self.twilio_sid = get_EV(ev="twilio_sid") # locate by logging in to Twilio website
        self.twilio_token = get_EV(ev="twilio_token") # locate by logging in to Twilio website
        self.twilio_from = get_EV(ev="twilio_from") # locate by logging in to Twilio website
        self.twilio_to = sort_twilio_to() # to where should texts/calls be sent
        self.icecast_user = get_EV(ev="icecast_user") # our icecast username
        self.icecast_pass = get_EV(ev="icecast_pass") # our icecast password
        self.pod_server_uname = get_EV(ev="pod_server_uname")

def get_EV(ev: str):
    try:
        ev = os.environ[ev]
        return ev
    except KeyError:
        raise RuntimeError(f"Missing required environment variable: {ev}")

def sort_destinations():
    destinations = get_EV(ev="destinations")
    destinations = destinations.split(",")
    destination_list = []
    for destination in destinations:
        destination = destination.split() #remove whitespace
        # the split() above returns a list, so we need to interate through it, even though it's only one string
        for dest in destination:
            destination_list.append(dest)
    return destination_list

def sort_to_email():
    to_emails = get_EV(ev="toEmail")
    to_emails = to_emails.split(",")
    to_email_list = []
    for email in to_emails:
        email = email.split()
        for i in email:
            to_email_list.append(i)
    return to_email_list

def sort_twilio_to():
    twilio_to_numbers = get_EV(ev="twilio_to")
    twilio_to_numbers = twilio_to_numbers.split(",")
    twilio_to_list = []
    for number in twilio_to_numbers:
        number = number.split()
        for num in number:
            twilio_to_list.append(num)
    return twilio_to_list
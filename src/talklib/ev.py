'''
These are all of the environment variables we're calling from the PC.
They'll be imported into the other files in this package.

We're using the file so we have one central place from which
to reference them.

If you're installing the talklib module on a PC for the first time, 
make sure all of these are declared in the PC's environment variables.

If you need to change them, you probably want to change them at the PC level, not here.
'''

import os

class EV:
    def __init__(self):
        self.destinations = [os.environ['OnAirPC'], os.environ['ProductionPC']]# where should output files go? MUST BE A LIST EVEN WITH ONLY ONE
        self.syslog_host = os.environ["syslog_server"] # ip of syslog server (PC with syslog software)
        self.fromEmail = os.environ['fromEmail']  # from where should emails appear to come?
        self.toEmail = os.environ['toEmail']  # to where should emails be sent?
        self.mail_server = os.environ["mail_server_external"]  # IP of mail server (ITS set this up for us)
        self.twilio_sid = os.environ['twilio_sid'] # locate by logging in to Twilio website
        self.twilio_token = os.environ['twilio_token']# locate by logging in to Twilio website
        self.twilio_from = os.environ['twilio_from'] # locate by logging in to Twilio website
        self.twilio_to = os.environ['twilio_to'] # to where should texts/calls be sent
        self.icecast_user = os.environ['icecast_user'] # our icecast username
        self.icecast_pass = os.environ['icecast_pass'] # our icecast password
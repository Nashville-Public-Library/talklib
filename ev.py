'''
These are all of the environment variables we're calling from the PC.
They'll be imported into the other files in this module.

We're using the file so we have one central place from which
to reference them.

If you're installing the talklib module on a PC for the first time, 
make sure all of these are declared in the PC's environment variables.

If you need to change them, change them at the PC level, not here.
'''

import os

destinations = [os.environ['OnAirPC'], os.environ['ProductionPC']] # where should output files go?
syslog_host = os.environ["syslog_server"] # ip of syslog server (PC with syslog software)
fromEmail = os.environ['fromEmail']  # from where should emails appear to come?
toEmail = os.environ['toEmail']  # to where should emails be sent?
mail_server = os.environ["mail_server_external"]  # IP of mail server (ITS set this up for us)
twilio_sid = os.environ['twilio_sid'] # locate by logging in to Twilio website
twilio_token = os.environ['twilio_token'] # locate by logging in to Twilio website
twilio_from = os.environ['twilio_from'] # locate by logging in to Twilio website
twilio_to = os.environ['twilio_to'] # to where should texts/calls be sent
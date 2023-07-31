from datetime import datetime
from email.message import EmailMessage
import ffmpeg
import logging
from logging.handlers import SysLogHandler
import os
import smtplib
import subprocess

from twilio.rest import Client

from talklib.ev import EV

def get_timestamp():
    timestamp = datetime.now().strftime('%H:%M:%S on %d %b %Y')
    return timestamp

def clear_screen():
    '''clears the terminal'''
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def print_to_screen(message):
    '''clear terminal and print message to screen.'''
    clear_screen()
    print(f'{message}\n')  # get user's attention!
    input('(press enter to close this window)') # force user to acknowledge by closing window

def today_is_weekday():
    '''crude mechanism for determining if today is a weekday.'''
    today = datetime.now().strftime('%a')
    weekend = ['Sat', 'Sun']
    if today not in weekend:
        return True
    else:
        return False

def send_call(message):
    '''send voice call via twilio'''
    client = Client(EV().twilio_sid, EV().twilio_token)

    call = client.calls.create(
                            twiml=f'<Response><Say>{message}</Say></Response>',
                            to=EV().twilio_to,
                            from_=EV().twilio_from
                        )
    call.sid

def send_sms(message):
    '''send sms via twilio. '''
    client = Client(EV().twilio_sid, EV().twilio_token)
    message = client.messages.create(
        body=message,
        from_=EV().twilio_from,
        to=EV().twilio_to
    )
    message.sid

def send_syslog(message: str):
    '''send message to syslog server'''
    port = int('514')
    my_logger = logging.getLogger('MyLogger')
    my_logger.setLevel(logging.DEBUG)
    handler = SysLogHandler(address=(EV().syslog_host, port))
    my_logger.addHandler(handler)

    my_logger.info(message)
    my_logger.removeHandler(handler) # don't forget this after you send the message!

def send_mail(message: str, subject: str):
    '''send email to TL gmail account via relay address'''
    format = EmailMessage()
    format.set_content(message)
    format['Subject'] = subject
    format['From'] = EV().fromEmail
    format['To'] = EV().toEmail

    mail = smtplib.SMTP(host=EV().mail_server)
    mail.send_message(format)
    mail.quit()

def get_length_in_minutes(file_to_check):
    duration = ffmpeg.probe(filename=file_to_check)
    duration = duration['format']['duration']
    
    # convert the number to something more usable/readable
    duration = float(duration)
    duration = duration/60
    duration = round(duration, 2)

    return duration
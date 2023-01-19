from datetime import datetime
import os
from twilio.rest import Client

from . import ev as tlev

twilio_sid = tlev.twilio_sid
twilio_token = tlev.twilio_token
twilio_from = tlev.twilio_from
twilio_to = tlev.twilio_to

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
    clear_screen()
    print(f'{message}\n')  # get user's attention!
    input('(press enter to close this window)') # force user to acknowledge by closing window

def today_is_weekday():
    today = datetime.now().strftime('%a')
    weekend = ['Sat', 'Sun']
    if today not in weekend:
        return True
    else:
        return False

def send_call(message):
    '''send voice call via twilio'''
    client = Client(twilio_sid, twilio_token)

    call = client.calls.create(
                            twiml=f'<Response><Say>{message}</Say></Response>',
                            to=twilio_to,
                            from_=twilio_from
                        )
    call.sid

def send_sms(message):
    '''
    send sms via twilio. 
    Several of these variables are environement variables, declared up top.
    '''
    client = Client(twilio_sid, twilio_token)
    message = client.messages.create(
        body=message,
        from_=twilio_from,
        to=twilio_to
    )
    message.sid
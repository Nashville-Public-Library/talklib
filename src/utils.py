from datetime import datetime
import os
from twilio.rest import Client

from src.ev import EV

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
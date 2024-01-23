from datetime import datetime
from email.message import EmailMessage
import ffmpeg
import logging
from logging.handlers import SysLogHandler
import os
import smtplib

from twilio.rest import Client

from talklib.ev import EV

def get_timestamp() -> str:
    timestamp = datetime.now().strftime('%H:%M:%S on %d %b %Y')
    return timestamp

def clear_screen() -> None:
    '''clears the terminal'''
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def print_to_screen_and_wait(message: str) -> None:
    '''clear terminal and print message to screen.'''
    clear_screen()
    print(f'{message}\n')  # get user's attention!
    input('(press enter to close this window)') # force user to acknowledge by closing window

def today_is_weekday() -> bool:
    '''crude mechanism for determining if today is a weekday.'''
    today = datetime.now().strftime('%a')
    weekend = ['Sat', 'Sun']
    if today not in weekend:
        return True
    else:
        return False

def get_length_in_minutes(file_to_check) -> float:
    duration = ffmpeg.probe(filename=file_to_check)
    duration = duration['format']['duration']
    
    # convert the number to something more usable/readable
    duration = float(duration)
    duration = duration/60
    duration = round(duration, 2)

    return duration
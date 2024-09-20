from datetime import datetime
import os

import requests

from talklib.notify import Notify

def get_timestamp() -> str:
    timestamp = datetime.now().strftime('%H:%M:%S on %d %b %Y')
    return timestamp

def clear_screen() -> None:
    '''clears the terminal'''
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def raise_exception_and_wait(message: str, error = Exception) -> None:
    '''clear terminal and print message to screen.'''
    clear_screen()
    print(f'{message}\n')  # get user's attention!
    input('(press enter to close this window)') # force user to acknowledge by closing window
    raise error (message)

def today_is_weekday() -> bool:
    '''crude mechanism for determining if today is a weekday.'''
    today = datetime.now().strftime('%a')
    weekend = ['Sat', 'Sun']
    if today not in weekend:
        return True
    else:
        return False
    
def metadata_to_icecast(title):
    notify = Notify()
    notify.syslog.send_syslog_message(message=f'attempting to send "{title}" to Icecast')
    user = os.environ['icecast_user']
    password = os.environ['icecast_pass']
    url = f'https://npl.streamguys1.com:80/admin/metadata?mount=/live&mode=updinfo&song={title}'
    send = requests.get(url, auth = (user, password))
    if send.status_code == 200:
        notify.syslog.send_syslog_message(message=f'Successfully sent "{title}" to Icecast') 
        return
    
    to_send = f'There was a problem sending metadata ({title}) to Icecast. The response code was: {send.status_code}'
    if today_is_weekday():
        notify.syslog.send_syslog_message(message=to_send, level='error')
        notify.send_mail(subject='Error', message=to_send)
    else:
        notify.syslog.send_syslog_message(message=to_send, level='error')
        notify.send_mail(subject='Error', message=to_send)
        notify.send_sms(message=to_send)
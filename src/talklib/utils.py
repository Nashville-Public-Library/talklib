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
    user = os.environ['icecast_user']
    password = os.environ['icecast_pass']
    URLs: tuple = (f'https://npl.streamguys1.com/admin/metadata?mount=/live&mode=updinfo&song={title}', 
                   f"https://stream.talkinglibrary.nashville.gov/admin/metadata?mount=/live_64_intro.mp3&mode=updinfo&song={title}")
    for url in URLs:
        try:
            notify.syslog.send_syslog_message(message=f'attempting to send "{title}" to {url}')
            send = requests.get(url, auth = (user, password))
            if send.status_code == 200:
                notify.syslog.send_syslog_message(message=f'Successfully sent "{title}" to {url}') 
                continue
            else: notify_on_metadata_problem(title=title, url=url, error=send.status_code)
            
        except Exception as e:
            notify_on_metadata_problem(title=title, url=url, error=e)

def notify_on_metadata_problem(title: str, url: str, error: str | int):
    notify = Notify()
    to_send = f'There was a problem sending metadata ({title}) to {url}: {error}'
    if today_is_weekday():
        notify.syslog.send_syslog_message(message=to_send, level='error')
        notify.send_mail(subject='Error', message=to_send)
    else:
        notify.syslog.send_syslog_message(message=to_send, level='error')
        notify.send_mail(subject='Error', message=to_send)
        notify.send_sms(message=to_send)
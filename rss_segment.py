'''
Check RSS feed for today's segment. If available, download 
audio file, convert to our format, and transfer to destination(s).
If not available, send notification.

This is for segments without a date attached.

© Nashville Public Library
© Ben Weddle is to blame for this code. Anyone is free to use it.
'''

import xml.etree.ElementTree as ET
import subprocess
from datetime import datetime
import shutil
import os
import logging
import logging.handlers
from logging.handlers import SysLogHandler
import smtplib
from email.message import EmailMessage
import time
from twilio.rest import Client
import urllib.request

#-----change these for each new program-----

show = 'Some Cool TL Segment' # for notifications
output_file = 'NameOfSegment.wav' #name of file
url = "http://somesite.org/somesegment.xml" #source rss feed

# these are for checking whether the length (in minutes!) of the file is outside of a range.
# decimal numbers are OK.
check_if_above = 0
check_if_below = 0

#*****----------SHOULD NOT NEED TO CHANGE ANYTHING BELOW THIS LINE----------*****

# these are defined in the PC's environement variables.
# If you need to change them, change them there, not here!
production_pc = os.environ["ProductionPC"] #Production PC
onair_pc = os.environ["OnAirPC"] #OnAir PC

short_day = datetime.now().strftime('%a') #used to match pubdate in rss feed, and other purposes.
timestamp = datetime.now().strftime('%H:%M:%S on %d %b %Y')

def convert_copy(input):
    '''convert with ffmpeg, check length, copy to destinations, remove files from this folder'''
    subprocess.run(f'ffmpeg -hide_banner -loglevel quiet -i {input} -ar 44100 -ac 1 -af loudnorm=I=-21 -y {output_file}')
    check_length() #check file length before deleting file from current directory
    shutil.copy(f'{output_file}', f'{production_pc}\{output_file}')
    shutil.copy(f'{output_file}', f'{onair_pc}\{output_file}')
    os.remove('input.mp3') #remove original file from current directory
    os.remove(f'{output_file}') #remove converted file from current directory

def download_file():
    '''download audio file from rss feed'''
    download = get_audio_url()
    input_file = 'input.mp3' #name the file we download
    subprocess.run(f'wget -q -O {input_file} {download}') #using wget because urlretrive is getting a 403 denied error
    check_downloaded_file(input_file=input_file)

def check_downloaded_file(input_file):
    filesize = os.path.getsize(input_file)
    is_not_empty = False
    i = 0
    while i < 3:
        if filesize > 0:
            convert_copy(input=input_file)
            is_not_empty = True
            break
        else:
            download_file()
            i = i+1
    if is_not_empty == True:
        pass
    else:
        to_send = (f"There was a problem with {show}.\n\n\
It looks like the downloaded file is empty. Please check manually! \n\n\
{timestamp}")
        notify(message=to_send , subject='Error')        

def syslog():
    '''send message to syslog server'''
    host = os.environ["syslog_server"] #IP of PC with syslog server software
    port = int('514')

    my_logger = logging.getLogger('MyLogger')
    my_logger.setLevel(logging.DEBUG)
    handler = SysLogHandler(address = (host, port))
    my_logger.addHandler(handler)

    my_logger.info(f'{show} was successfully processed. All is well.')

def send_mail(message, subject):
    '''send email to TL gmail account via relay address'''
    mail_server = os.environ["mail_server_external"] #IP of mail server
    format = EmailMessage()
    format.set_content(message)
    format['Subject'] = f'{subject}: {show}'
    format['From'] = "ben.weddle@nashville.gov"
    format['To'] = "nashvilletalkinglibrary@nashville.gov"

    mail = smtplib.SMTP(host=mail_server)
    mail.send_message(format)
    mail.quit()

def send_sms(message):
    '''send sms via twilio. all info is stored in PC's environement variables'''
    twilio_sid = os.environ.get('twilio_sid')
    twilio_token = os.environ.get('twilio_token')
    twilio_from = os.environ.get('twilio_from')
    twilio_to = os.environ.get('twilio_to')

    client = Client(twilio_sid, twilio_token)

    message = client.messages.create(
                        body = message,
                        from_= twilio_from,
                        to = twilio_to
                        )
    message.sid

def notify(message, subject):
    weekend = ['Sat', 'Sun']
    if short_day in weekend:
        send_sms(message=message) 
        send_mail(message=message, subject=subject)
    else:
        send_mail(message=message, subject=subject)

def check_file_transferred():
    '''check if file transferred to OnAir PC'''
    try: #if file exists, send syslog message
        os.path.isfile(f'{onair_pc}\{output_file}')
        syslog()
    except: #if file doesn't exist, send notification
        to_send = (f"There was a problem with {show}.\n\n\
It looks like the file either wasn't converted or didn't transfer correctly. \
Please check manually! \n\n\
    {timestamp}")
        notify(message=to_send, subject='Error')
        os.system('cls')
        print(to_send) #get user's attention!
        print()
        input('(press enter to close this window)')#force user to acknowledge by closing window

def check_length():
    '''check length of converted file with ffprobe. if too long or short, send notification'''
    duration = subprocess.getoutput(f"ffprobe -v error -show_entries format=duration \
    -of default=noprint_wrappers=1:nokey=1 {output_file}")
    duration = float(duration)
    duration = round(duration)
    duration = duration/60
    
    if duration > check_if_above:
        to_send = (f"Today's {show} is {duration} minutes long! \
Please check manually and make edits to bring it below {check_if_above} minutes.\n\n\
{timestamp}")
        notify(message=to_send, subject='Check Length')
    elif duration < check_if_below:
        to_send = (f"Today's {show} is only {duration} minutes long! \
This is unusual and could indicate a problem with the file. Please check manually!\n\n\
{timestamp}")
        notify(message=to_send, subject='Check Length')
    else: pass

def get_feed():
    '''check if today's file has been uploaded'''
    header = {'User-Agent': 'Darth Vader'} #requests are denied unless user agent is sent
    req = urllib.request.Request(url, None, header)
    html = urllib.request.urlopen(req)
    html = html.read()
    root = ET.fromstring(html)
    return root

def check_feed_updated():
    root = get_feed()
    for t in root.findall('channel'):
        item = t.find('item') #'find' only returns the first match!
        pub_date = item.find('pubDate').text
        if short_day in pub_date:
            feed_updated = True
            return feed_updated

def get_audio_url():
    root = get_feed()
    for t in root.findall('channel'):
        item = t.find('item') #'find' only returns the first match!
        audio_url = item.find('enclosure').attrib
        audio_url = audio_url.get('url')
        return audio_url

def check_feed_loop():
    '''for some reason the first time we check the feed, it is not showing as updated.
    It's being cached, or something...? So we are checking it 3 times, for good measure.'''
    i = 0
    while i < 3:
        feed_updated = check_feed_updated()
        if feed_updated == True:
            return feed_updated
        else: 
            time.sleep(1)
            i = i+1

#BEGIN
print(f"I'm working on {show}. Just a moment...")
feed_updated = check_feed_loop()
if feed_updated == True:
    download_file()
    check_file_transferred()
else:
    to_send = (f"There was a problem with {show}. \n\n\
It looks like today's file hasn't yet been posted. \
Please check and download manually! Yesterday's file will remain.\n\n\
{timestamp}")
    notify(message=to_send, subject='Error')
    os.system('cls')
    print(to_send)
    print()
    input('(press enter to close this window)') #force user to acknowledge by closing window

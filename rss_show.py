'''
Check RSS feed for today's show. If available, download 
audio file, convert to our format, and transfer to destination(s).
If not available, send notification.

This is for daily shows with a date. EG WSJ-042022

© Nashville Public Library
© Ben Weddle is to blame for this code. Anyone is free to use it.
'''
import xml.etree.ElementTree as ET
import subprocess
from datetime import datetime
import shutil
import os
import glob
import logging
import logging.handlers
from logging.handlers import SysLogHandler
import smtplib
from email.message import EmailMessage
import time
from twilio.rest import Client
import urllib.request

#-----change these for each new program-----

show = 'Some Cool TL Program' #name of show.
show_abbr = 'SomeProgram' #filename of show without date (do not include the dash!). EG NYT
url = "http://somesite.org/somerssfeed.xml" #source RSS feed

# these are for checking whether the length (in minutes!) of the file is outside of a range.
# decimal numbers are OK.
check_if_above = 0
check_if_below = 0

'''
*****----------SHOULD NOT NEED TO CHANGE ANYTHING BELOW THIS LINE----------*****
'''

# these are defined in the PC's environement variables.
# If you need to change them, change them there, not here!
production_pc = os.environ["ProductionPC"]
onair_pc = os.environ["OnAirPC"]

timestamp = datetime.now().strftime('%H:%M:%S on %d %b %Y')

def convert_copy():
    '''download file, convert with ffmpeg, check length, copy to destinations, remove files from this folder'''
    date = datetime.now().strftime("%m%d%y")
    global filename
    filename = (f"{show_abbr}-{date}.wav")
    subprocess.run(f'wget -q -O input.mp3 {download}') #using wget because urlretrive is getting a 403 denied error
    subprocess.run(f'ffmpeg -hide_banner -loglevel quiet -i input.mp3 -ar 44100 -ac 1 -af loudnorm=I=-21 -y {filename}')
    check_length() #check file length before deleting file from current directory
    shutil.copy(f'{filename}', f'{production_pc}\{filename}')
    shutil.copy(f'{filename}', f'{onair_pc}\{filename}')
    os.remove('input.mp3') #remove original file from current directory
    os.remove(f'{filename}') #remove converted file from current directory

def remove_old_files():
    '''delete yesterday's files from destinations. 
    OK to use glob wildcards since there should only ever be one file'''
    for old_file in glob.glob(f'{production_pc}\{show_abbr}*.wav'):
        os.remove(old_file)
    for old_file in glob.glob(f'{onair_pc}\{show_abbr}*.wav'):
        os.remove(old_file)

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
    #TODO: explain why we're sending mail this way

def send_sms(message):
    '''send sms via twilio'''
    twilio_sid = os.environ['twilio_sid']
    twilio_token = os.environ['twilio_token']
    twilio_from = os.environ['twilio_from']
    twilio_to = os.environ['twilio_to']

    client = Client(twilio_sid, twilio_token)
    message = client.messages.create(
                        body = message,
                        from_= twilio_from,
                        to = twilio_to
                        )
    message.sid

def notify(message, subject):
    '''if today is on a weekend, send sms and email. if not, send email only'''
    today_short = datetime.now().strftime('%a')
    weekend = ['Sat', 'Sun']
    if today_short in weekend:
        send_sms(message)
        send_mail(message, subject)
    else:
        send_mail(message, subject)

def check_file_exists():
    '''check if file transferred to OnAir PC'''
    try: #if file exists, send syslog message
        os.path.isfile(f'{onair_pc}\{filename}')
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
        input('(press enter to close this window)') #force user to acknowledge

def check_length():
    '''check length of converted file with ffprobe. if too long or short, send notification'''
    duration = subprocess.getoutput(f"ffprobe -v error -show_entries format=duration \
    -of default=noprint_wrappers=1:nokey=1 {filename}")
    duration = float(duration)
    duration = duration/60
    duration = round(duration, 2)
    
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

def check_feed():
    '''check if today's file has been uploaded'''
    header = {'User-Agent': 'Darth Vader'} #identify yourself or request may be rejected!
    req = urllib.request.Request(url, None, header)
    rss = urllib.request.urlopen(req)
    rss = rss.read()
    root = ET.fromstring(rss)
    global feed_updated
    feed_updated = False
    for t in root.findall('channel'):
        today_short = datetime.now().strftime('%a')
        item = t.find('item') #'find' only returns the first match!
        pub_date = item.find('pubDate').text
        global download
        download = item.find('enclosure').attrib
        download = download.get('url')
        if today_short in pub_date:
            feed_updated = True

def check_feed_loop():
    '''for some reason the first time we check the feed, it is not showing as updated.
    It's being cached, or something...? So we are checking it 3 times, for good measure.'''
    i = 0
    while i <3:
        check_feed()
        if feed_updated == True:
            break
        else: 
            time.sleep(1)
            i = i+1

#BEGIN
print(f"I'm working on {show}. Just a moment...")
check_feed_loop()

# if feed is updated, continue. if not, send notification.
if feed_updated == True:
    remove_old_files()
    convert_copy()
    check_file_exists()
else:
    to_send = (f"There was a problem with {show}. \n\n\
It looks like today's file hasn't yet been posted. \
Please check and download manually!\n\n\
{timestamp}")
    notify(message=to_send, subject='Error')
    os.system('cls')
    print(to_send)
    print()
    input('(press enter to close this window)') #force user to acknowledge

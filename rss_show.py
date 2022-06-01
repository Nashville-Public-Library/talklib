'''
Check RSS feed for today's segment. If available, download 
audio file, convert to TL format, and transfer to destination(s).
If not available, send notification.

This is for daily shows with a date. EG WSJ-042022.wav

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
import requests
import glob

#-----change these for each new program-----

show = 'Some cool TL Show' #name of show.
showAbbr = 'SomeShow' #filename of show without date (do not include the dash!). EG NYT, WSJ, etc.
url = "http://somesite.org/somefeed.rss" #source RSS feed

# these are for checking whether the length (in minutes!) of the file is outside of a range.
# used for notification only
# decimal numbers are OK.
check_if_above = 0.0
check_if_below = 0.0

'''
    -------------------------------------------------------------------------------
        ----------SHOULD NOT NEED TO CHANGE ANYTHING BELOW THIS LINE----------
    -------------------------------------------------------------------------------
'''

# these are defined in the PC's environement variables.
# If you need to change them, change them there, not here!
destinations = [os.environ['OnAirPC'], os.environ['ProductionPC']]
fromEmail = os.environ['fromEmail'] #from where should emails appear to come?
toEmail = os.environ['toEmail'] #to where should emails be sent?

short_day = datetime.now().strftime('%a')
timestamp = datetime.now().strftime('%H:%M:%S on %d %b %Y')

def convert(input):
    '''convert file with ffmpeg and call check length and copy functions'''
    date = datetime.now().strftime("%m%d%y")
    outputFile = (f"{showAbbr}-{date}.wav")
    syslog(message=f'{show}: Converting to TL format.')
    subprocess.run(f'ffmpeg -hide_banner -loglevel quiet -i {input} -ar 44100 -ac 1 -af loudnorm=I=-21 -y {outputFile}')
    check_length(fileToCheck=outputFile)
    remove(fileToDelete=input) #call this before removing the files
    copy(fileToCopy=outputFile)

def copy(fileToCopy):
    '''TODO explain'''
    numberOfDestinations = len(destinations)
    numberOfDestinations = numberOfDestinations -1
    while numberOfDestinations >= 0:
        syslog(message=f'{show}: Copying to {destinations[numberOfDestinations]}...')
        shutil.copy(fileToCopy, destinations[numberOfDestinations])
        numberOfDestinations = numberOfDestinations-1
    remove(fileToDelete=fileToCopy)
    check_file_transferred(fileToCheck=fileToCopy)

def remove(fileToDelete):
    '''TODO explain'''
    syslog(message=f'{show}: Deleting {fileToDelete} from current directory...')
    os.remove(fileToDelete) #remove original file from current directory

def removeYesterdayFiles():
    '''delete yesterday's files from destinations. 
    OK to use glob wildcards since there should only ever be one file'''
    numberOfDestinations = len(destinations)
    numberOfDestinations = numberOfDestinations -1
    while numberOfDestinations >= 0:
        for yesterdayFile in glob.glob(f'{destinations[numberOfDestinations]}\{showAbbr}*.wav'):
            syslog(message=f"{show}: Removing yesterday's files from {destinations[numberOfDestinations]}...")
            os.remove(yesterdayFile)
            numberOfDestinations = numberOfDestinations-1

def download_file():
    '''download audio file from rss feed'''
    download = get_audio_url()
    syslog(message=f'{show}: Attempting to download audio file.')
    input_file = 'input.mp3' #name the file we download
    subprocess.run(f'wget -q -O {input_file} {download}') #using wget because urlretrive is getting a 403 denied error
    check_downloaded_file(fileToCheck=input_file)

def check_downloaded_file(fileToCheck):
    '''TODO explain'''
    filesize = os.path.getsize(fileToCheck)
    is_not_empty = False
    i = 0
    while i < 3:
        if filesize > 0:
            syslog(message=f'{show} is not empty. Continuing...')
            convert(input=fileToCheck)
            is_not_empty = True
            break
        else:
            syslog(message=f'{show} is empty. Will download again. Attempt # {i}.')
            download_file()
            i = i+1
    if is_not_empty == True:
        pass
    else:
        to_send = (f"There was a problem with {show}.\n\n\
It looks like the downloaded file is empty. Please check manually! \
Yesterday's file will remain. \n\n\
{timestamp}")
        notify(message=to_send , subject='Error')        

def syslog(message):
    '''send message to syslog server'''
    host = os.environ["syslog_server"] #IP of PC with syslog server software
    port = int('514')

    my_logger = logging.getLogger('MyLogger')
    my_logger.setLevel(logging.DEBUG)
    handler = SysLogHandler(address = (host, port))
    my_logger.addHandler(handler)

    my_logger.info(message)
    my_logger.removeHandler(handler) #don't forget this after you send the message!

def send_mail(message, subject):
    '''send email to TL gmail account via relay address'''
    mail_server = os.environ["mail_server_external"] #IP of mail server
    format = EmailMessage()
    format.set_content(message)
    format['Subject'] = f'{subject}: {show}'
    format['From'] = fromEmail
    format['To'] = toEmail

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
    '''TODO: explain'''
    weekend = ['Sat', 'Sun']
    if short_day in weekend:
        send_sms(message=message) 
        send_mail(message=message, subject=subject)
        syslog(message=message)
    else:
        send_mail(message=message, subject=subject)
        syslog(message=message)

def check_file_transferred(fileToCheck):
    '''check if file transferred to OnAir PC'''
    try:
        numberOfDestinations = len(destinations)
        numberOfDestinations = numberOfDestinations -1
        while numberOfDestinations >= 0:
            os.path.isfile(f'{destinations[numberOfDestinations]}\{fileToCheck}')
            numberOfDestinations = numberOfDestinations-1
            syslog(message=f'{show}: File arrived at {destinations[numberOfDestinations]}')
    except:
        to_send = (f"There was a problem with {show}.\n\n\
It looks like the file either wasn't converted or didn't transfer correctly. \
Please check manually! \n\n\
    {timestamp}")
        notify(message=to_send, subject='Error')
        subprocess.run('cls', shell=True)
        print(to_send) #get user's attention!
        print()
        input('(press enter to close this window)')#force user to acknowledge by closing window

def check_length(fileToCheck):
    '''check length of converted file with ffprobe. if too long or short, send notification'''
    duration = subprocess.getoutput(f"ffprobe -v error -show_entries format=duration \
    -of default=noprint_wrappers=1:nokey=1 {fileToCheck}")
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
    else:
        syslog(message=f'{show}: File is {duration} minute(s). Continuing...')

def get_feed():
    '''check if today's file has been uploaded'''
    header = {'User-Agent': 'Darth Vader'} #usually helpful to identify yourself
    rssfeed = requests.get(url, headers=header)
    rssfeed = rssfeed.text
    rssfeed = ET.fromstring(rssfeed)
    return rssfeed

def check_feed_updated():
    '''TODO explain'''
    root = get_feed()
    for t in root.findall('channel'):
        item = t.find('item') #'find' only returns the first match!
        pub_date = item.find('pubDate').text
        if short_day in pub_date:
            syslog(message=f'{show}: The feed is updated. Continuing...')
            return True

def get_audio_url():
    '''TODO: explain'''
    root = get_feed()
    for t in root.findall('channel'):
        item = t.find('item') #'find' only returns the first match!
        audio_url = item.find('enclosure').attrib
        audio_url = audio_url.get('url')
        syslog(message=f'{show}: Audio URL is: {audio_url}')
        return audio_url

def check_feed_loop():
    '''for some reason the first time we check the feed, it is not showing as updated.
    It's being cached, or something...? So we are checking it 3 times, for good measure.'''
    i = 0
    while i < 3:
        syslog(message=f'{show}: Attempt {i} to check feed.')
        feed_updated = check_feed_updated()
        if feed_updated == True:
            return feed_updated
        else:
            time.sleep(1)
            i = i+1

#BEGIN
toSend = (f"I'm working on {show}. Just a moment...")
print(toSend)
syslog(message=toSend)

if check_feed_loop() == True:
    removeYesterdayFiles()
    download_file()
else:
    to_send = (f"There was a problem with {show}. \n\n\
It looks like today's file hasn't yet been posted. \
Please check and download manually! Yesterday's file will remain.\n\n\
{timestamp}")
    notify(message=to_send, subject='Error')
    subprocess.run('cls', shell=True)
    print(to_send)
    print()
    input('(press enter to close this window)') #force user to acknowledge

'''
TL library for processing RSS shows and other segments.
It's best to read the docs.

© Nashville Public Library
© Ben Weddle is to blame for this code. Anyone is free to use it.
'''

from datetime import datetime
import glob
import os
import shutil
import time
import xml.etree.ElementTree as ET

import ffmpeg
import requests

from talklib.ev import EV
from talklib.notify import Notify
from talklib.utils import get_timestamp, clear_screen, print_to_screen_and_wait, today_is_weekday, get_length_in_minutes
from talklib.ffmpeg import FFMPEG


class TLShow():
    '''TODO write something here'''
    def __init__(self):

        self.show:str = None
        self.show_filename: str = None
        self.url: str = None
        self.is_permalink: int | float = 0
        self.include_date: bool = False
        self.remove_yesterday: bool = False
        self.is_local: str = None
        self.local_file: str = None
        self.remove_source: bool = False
        self.check_if_above: int | float = 0    
        self.check_if_below: int | float = 0
        self.notifications = Notify()
        self.ffmpeg = FFMPEG()
        self.destinations: list = EV().destinations
    
    
    def __str__(self) -> str:
        return "This is a really cool, useful thing. Calling this should give useful info. I'll come back to it. TODO"
    
    def six_digit_date_string(self) -> str:
        date = datetime.now().strftime("%m%d%y")
        return date
    
    def create_output_filename(self) -> str:
        '''returns the audio filename to use depending on whether we should include the date'''
        if self.include_date:
            date = TLShow.six_digit_date_string(self)
            outputFile = (f"{self.show_filename}-{date}.wav")
        else:
            outputFile = (f'{self.show_filename}.wav')
        return outputFile

    def convert(self, input):
        ffmpeg = self.ffmpeg
        ffmpeg.input_file = input
        ffmpeg.output_file = self.create_output_filename()
        self.prep_syslog(message='preparing to convert')
        ffmpeg_commands = ffmpeg.get_commands()
        self.prep_syslog(message=f'FFmpeg commands: {ffmpeg_commands}')
        try:
            file = ffmpeg.convert()
            self.prep_syslog(message='file converted successfully')
            return file
        except Exception as ffmpeg_exception:
            self.send_notifications(message=ffmpeg_exception, subject='Error')
            self.prep_syslog(message=f'conversion failed: {ffmpeg_exception}')
            raise Exception (ffmpeg_exception)


    def copy_then_remove(self, fileToCopy):
        '''TODO explain'''
        
        for destination in self.destinations:
            TLShow.prep_syslog(self, message=f'Copying {fileToCopy} to {destination}...')
            shutil.copy(fileToCopy, destination)

        #this is the file we're copying, so it is the file already converted. we always want to remove this.
        TLShow.remove(self, fileToDelete=fileToCopy, is_output_file=True)

    def decide_whether_to_remove(self) -> bool:
        '''
        url shows should always remove the "source" files,
        since these are the files downloaded from the internet.
        local shows are downloaded ahead of time. we do not necessarily 
        want to delete these.
        delete this line (don't ask).
        '''
        if self.url:
            return True
        elif self.local_file:
            if self.remove_source == True:
                return True 
            else:
                return False

    def remove(self, fileToDelete, is_output_file: bool=False):
        '''TODO explain'''
        if TLShow.decide_whether_to_remove(self) or is_output_file:
            TLShow.prep_syslog(self, message=f'Deleting {fileToDelete}')
            try:
                os.remove(fileToDelete)
            except Exception as e:
                self.prep_syslog(message=e)

    def remove_yesterday_files(self):
        '''
        delete yesterday's files from destinations. 
        OK to use glob wildcards since there should only ever be one file
        '''
        if self.remove_yesterday:
            for destination in self.destinations:
                matched_filenames = glob.glob(f'{destination}/{self.show_filename}*.wav')
                if matched_filenames:
                    for file in matched_filenames:
                        TLShow.prep_syslog(self, message=f'Deleting existing matched file: {file}')
                        os.remove(f'{file}')
                else:
                    TLShow.prep_syslog(self, message=f"{self.show}: Cannot find existing matched files in {destination}. Continuing...")

    def download_file(self):
        '''
        Download audio file from RSS feed or permalink.
        If this is a permalink show, we can just use the URL. BUT
        if this is an RSS show, the URL links to an RSS feed, so 
        we need to call the function for that.

        please split these into separate functions, one for permalink 
        and one for RSS. or implement some other method to test against
        a user declaring URL & is_permalink with an RSS URL, which
        currently will throw an error.
        '''
        if self.is_permalink:
            download_URL = self.url
        else:
            download_URL = TLShow.get_RSS_audio_url(self)

        TLShow.prep_syslog(self, message=f'Attempting to download audio file.')
        input_file = 'input.mp3'  # name the file we download
        with open (input_file, mode='wb') as downloaded_file:
            a = requests.get(download_URL)
            downloaded_file.write(a.content)
            downloaded_file.close()
        
        TLShow.prep_syslog(self, message=f'File downloaded successfully in {os.getcwd()}.')
        return downloaded_file.name

    def check_downloaded_file(self, fileToCheck, how_many_attempts):
        '''TODO explain'''
        try:
            filesize = os.path.getsize(fileToCheck)
        except FileNotFoundError as error:
            TLShow.send_notifications(self, message=f'It looks like the file does not exist. Here is the error: {error}', subject='Error')
            raise FileNotFoundError
            
        is_not_empty = False
        while how_many_attempts < 3:
            if filesize > 0:
                TLShow.prep_syslog(self, message='File is not empty. Continuing...')
                is_not_empty = True
                return True
            else:
                TLShow.prep_syslog(self, message=f'File is empty. Will download again. Attempt # {how_many_attempts}.')
                how_many_attempts = how_many_attempts+1
                TLShow.download_file(self)
                TLShow.check_downloaded_file(self, fileToCheck=fileToCheck, how_many_attempts=how_many_attempts)
        if not is_not_empty:
            toSend = (
f"There was a problem with {self.show}.\n\n\
It looks like the downloaded file is empty. Please check manually! Yesterday's file will remain.\n\n\
{get_timestamp()}"
)
            TLShow.send_notifications(self, message=toSend, subject='Error')
            TLShow.remove(self, fileToDelete=fileToCheck)
            raise Exception (toSend)
            
    def prep_syslog(self, message: str):
        '''send message to syslog server'''
        message = f'{self.show}: {message}'
        self.notifications.send_syslog(message=message)


    def prep_send_mail(self, message: str, subject: str):
        '''send email to TL gmail account via relay address'''
        subject = f'{subject}: {self.show}'
        self.notifications.send_mail(subject=subject, message=message)

    def send_sms_if_enabled(self, message: str):
        '''send sms via twilio IF twilio_enable is set to True'''
        self.notifications.send_sms(message=message)

    def send_notifications(self, message: str, subject: str):
        '''we generally only want to send SMS via Twilio if today is on a weekend'''
        if today_is_weekday():
            TLShow.prep_send_mail(self, message=message, subject=subject)
            TLShow.prep_syslog(self, message=message)
        else:
            TLShow.send_sms_if_enabled(self, message=message)
            TLShow.prep_send_mail(self, message=message, subject=subject)
            TLShow.prep_syslog(self, message=message)

    def check_file_transferred(self, fileToCheck):
        '''check if file transferred to destination(s)'''
        numberOfDestinations = len(self.destinations) - 1
        success = False
        while numberOfDestinations >= 0:
            if os.path.isfile(f'{self.destinations[numberOfDestinations]}/{fileToCheck}'):
                numberOfDestinations = numberOfDestinations-1
                TLShow.prep_syslog(self, message=f'{fileToCheck} arrived at {self.destinations[numberOfDestinations]}')
                success = True
            else:
                toSend = (f"There was a problem with {self.show}.\n\n\
It looks like the file either wasn't converted or didn't transfer correctly. \
Please check manually!\n\n\
{get_timestamp()}")
                TLShow.send_notifications(self, message=toSend, subject='Error')
                print_to_screen_and_wait(message=toSend)
                break
        if success:
            TLShow.countdown(self)

    def check_length(self, fileToCheck):
        '''
        Check length of converted file with ffprobe. if too long or short, send notification.
        Notice we do not raise exceptions or halt execution. This is strictly for checking/notifying and
        troubleshooting afterwards. Do not raise exceptions here.
        '''
        # if these are not declared, don't run this check.
        if not (self.check_if_below and self.check_if_above):
            TLShow.prep_syslog(self, message='The check length function is turned off.')
        else:
            TLShow.prep_syslog(self, message=f'Checking whether length is between \
{self.check_if_below} and {self.check_if_above}')

            duration = get_length_in_minutes(file_to_check=fileToCheck)

            if duration > self.check_if_above:
                toSend = (f"Today's {self.show} is {duration} minutes long! \
Please check manually and make edits to bring it below {self.check_if_above} minutes.\n\n\
{get_timestamp()}")
                TLShow.send_notifications(self, message=toSend, subject='Check Length')

            elif duration < self.check_if_below:
                toSend = (f"Today's {self.show} is only {duration} minutes long! \
This is unusual and could indicate a problem with the file. Please check manually!\n\n\
{get_timestamp()}")
                TLShow.send_notifications(self, message=toSend, subject='Check Length')

            else:
                TLShow.prep_syslog(self, message=f'File is {duration} minute(s). Continuing...')
            
            return duration

    def get_feed(self):
        '''get the feed and create an ET object, which can then be called from other functions.'''
        try:
            header = {'User-Agent': 'Darth Vader'}  # usually helpful to identify yourself
            rssfeed = requests.get(self.url, headers=header)
            rssfeed = rssfeed.text
            rssfeed = ET.fromstring(rssfeed)
            return rssfeed
        except Exception as a:
            to_send = (
f"There's a Problem with {self.show}. It looks like the issue is with the URL/feed. \
Here's the error: {a}\n\n\
Is this a permalink show? Did you forget to set the is_permalink attribute?\n\n\
{get_timestamp()}"
                )
            TLShow.send_notifications(self, subject='Error', message=to_send)
            raise Exception (a)

    def check_feed_updated(self) -> bool:
        '''
        get the ET object from the get_feed function, 
        then parse through it to check whether there is an entry with today's date.
        If yes, return True.

        The format for this date is a standard format (E.G. '17 Oct 2022') set by 
        a standards organization. Most podcasts/RSS feeds follow this standard.
        '''
        root = TLShow.get_feed(self)
        for t in root.findall('channel'):
            item = t.find('item')  # 'find' only returns the first match!
            pub_date = item.find('pubDate').text
            today = datetime.now().strftime("%a, %d %b %Y")
            if today in pub_date:
                TLShow.prep_syslog(self, message='The feed is updated.')
                return True

    def get_RSS_audio_url(self) -> str:
        '''TODO: explain'''
        root = TLShow.get_feed(self)
        for t in root.findall('channel'):
            item = t.find('item')  # 'find' only returns the first match!
            audio_url = item.find('enclosure').attrib
            audio_url = audio_url.get('url')
            TLShow.prep_syslog(self, message=f'Audio URL is: {audio_url}')
            return audio_url

    def check_feed_loop(self) -> str:
        '''
        occasionally, the first time we check the feed, it is not showing as updated.
        It's being cached, or something...? So we are checking it 3 times, for good measure.
        '''
        i = 0
        feed_updated = False
        while i < 3:
            TLShow.prep_syslog(self, message=f'Attempt {i} to check feed.')
            feed_updated = TLShow.check_feed_updated(self)
            if feed_updated:
                break
            else:
                time.sleep(1)
                i = i+1
        return feed_updated

    def countdown(self):
        '''
        the reason for this is to give a visual cue to the user
        that the script has finished and is about to exit.
        Otherwise, the user does not know what happened; they
        just see the screen disappear.
        '''
        clear_screen()
        to_send = 'All Done.'
        TLShow.prep_syslog(self, message=to_send)
        print(f'{to_send}\n')
        number = 5
        i = 0
        while i < number:
            print(f'This window will close in {number} seconds...', end='\r')
            number = number-1
            time.sleep(1)

    def check_str_and_bool_type(attrib_to_check, type_to_check: str | bool, attrib_return: str):
        '''
        we are checking whether an attribute is either type str or bool, depending on what is passed in.
        
        'attrib_return' is solely for printing the message back out to the screen/log,
        it is not needed for the actual type check.
        (I can't figure out how else to get the name of the attribute)
        '''
        if  type(attrib_to_check) != type_to_check:
            raise Exception (f"Sorry, '{attrib_return}' attribute must be type: {type_to_check}, but you used {type(attrib_to_check)}.")

    def check_int_and_float_type(attrib_to_check, attrib_return: str):
        '''
        Attributes passed here can be either int or float.
        '''
        if not (type(attrib_to_check) == int or type(attrib_to_check) == float):
            raise Exception (f'Sorry, the {attrib_return} attribute must be a valid number (without quotes).')

    def check_attributes_are_valid(self):
        '''
        Run some checks on the attributes the user has set. I.E. the required
        attributes have been set, they are the right type, etc.
        '''
        TLShow.prep_syslog(self, message='checking user defined attributes')

        if not self.show:
            raise Exception ('Sorry, you need to specify a name for the show.')
        else:
            TLShow.check_str_and_bool_type(attrib_to_check=self.show, type_to_check=str, attrib_return='show')

        if not self.show_filename:
            raise Exception ('Sorry, you need to specify a filename for the show.')
        else:
            TLShow.check_str_and_bool_type(attrib_to_check=self.show_filename, type_to_check=str, attrib_return='show_filename')

        if not self.url:
            if not self.is_local:
                raise Exception('Sorry, you need to specify either a URL or a local file')

        if self.url and self.is_local:
            raise Exception ('Sorry, you cannot specify both a URL and a local audio file. You must choose only one.')
        
        if self.url and self.local_file:
            raise Exception ('Sorry, you cannot specify both a URL and a local audio file. You must choose only one.')

        if self.url:
            TLShow.check_str_and_bool_type(attrib_to_check=self.url, type_to_check=str, attrib_return='url')
        
        if self.is_local:
            TLShow.check_str_and_bool_type(attrib_to_check=self.is_local, type_to_check=bool, attrib_return='is_local')

        if self.local_file:
            TLShow.check_str_and_bool_type(attrib_to_check=self.local_file, type_to_check=str, attrib_return='local_file')
        
        if self.ffmpeg.breakaway:
            TLShow.check_int_and_float_type(attrib_to_check=self.ffmpeg.breakaway, attrib_return='breakaway')
        
        if self.ffmpeg.compression_level:
            TLShow.check_int_and_float_type(attrib_to_check=self.ffmpeg.compression_level, attrib_return='fflevel')

        if self.is_permalink:
            TLShow.check_str_and_bool_type(attrib_to_check=self.is_permalink, type_to_check=bool, attrib_return='is_permalink')

        if not (self.check_if_above and self.check_if_below):
            print('\n(You did not specify check_if_below and/or check_if_above. These checks will not be run.')
        
        if self.check_if_above:
            TLShow.check_int_and_float_type(attrib_to_check=self.check_if_above, attrib_return='check_if_above')
        
        if self.check_if_below:
            TLShow.check_int_and_float_type(attrib_to_check=self.check_if_below, attrib_return='check_if_below')
        
        if self.notifications.syslog_enable:
            TLShow.check_str_and_bool_type(attrib_to_check=self.notifications.syslog_enable, type_to_check=bool, attrib_return='notifications')

        if self.notifications.twilio_enable:
            TLShow.check_str_and_bool_type(attrib_to_check=self.notifications.twilio_enable, type_to_check=bool, attrib_return='twilio_enable')
        
        if self.notifications.email_enable:
            TLShow.check_str_and_bool_type(attrib_to_check=self.notifications.email_enable, type_to_check=bool, attrib_return='twilio_enable')

    def run(self):
        '''begins to process the file'''

        TLShow.prep_syslog(self, message=f'Starting script')
        print(f"I'm working on {self.show}. Just a moment...\n")

        TLShow.check_attributes_are_valid(self)

        if self.url and self.is_permalink:
            TLShow.prep_syslog(self, message='permalink show detected')
            TLShow.run_URL_permalink(self)

        # if url but not permalink, it must be an RSS feed...right?
        elif self.url:
            TLShow.prep_syslog(self, message='URL show detected')
            TLShow.run_URL_RSS(self)

        elif self.is_local:
            TLShow.prep_syslog(self, message='local show detected')
            TLShow.run_local(self)
                   
        else:
            raise Exception ('Sorry, something bad happened')

    def run_URL_permalink(self):
        # if url is declared, it's either an RSS or permalink show
        if self.url and self.is_permalink:
            TLShow.remove_yesterday_files(self)
            downloaded_file = TLShow.download_file(self)
            if TLShow.check_downloaded_file(self, fileToCheck=downloaded_file, how_many_attempts=0):
                output_file = TLShow.convert(self, input=downloaded_file)
            TLShow.check_length(self, fileToCheck=output_file)
            TLShow.remove(self, fileToDelete=downloaded_file)
            TLShow.copy_then_remove(self, fileToCopy=output_file)
            TLShow.check_file_transferred(self, fileToCheck=output_file)

    def run_URL_RSS(self):
        if TLShow.check_feed_loop(self):
            TLShow.remove_yesterday_files(self)
            downloaded_file = TLShow.download_file(self)
            if TLShow.check_downloaded_file(self, fileToCheck=downloaded_file, how_many_attempts=0):
                output_file = TLShow.convert(self, input=downloaded_file)
            TLShow.check_length(self, fileToCheck=output_file)
            TLShow.remove(self, fileToDelete=downloaded_file)
            TLShow.copy_then_remove(self, fileToCopy=output_file)
            TLShow.check_file_transferred(self, fileToCheck=output_file)
        else:
            toSend = (
f"There was a problem with {self.show}.\n\n\
It looks like today's file hasn't yet been posted. Please check and download manually! Yesterday's file will remain.\n\n\
{get_timestamp()}"
                )
            TLShow.send_notifications(self, message=toSend, subject='Error')
            print_to_screen_and_wait(message=toSend)
            raise Exception
    
    def run_local(self):
        if self.local_file:
            if TLShow.check_downloaded_file(self, fileToCheck=self.local_file, how_many_attempts=0):
                output_file = TLShow.convert(self, input=self.local_file)
            TLShow.check_length(self, fileToCheck=output_file)
            TLShow.remove(self, fileToDelete=self.local_file)
            TLShow.copy_then_remove(self, fileToCopy=output_file)
            TLShow.check_file_transferred(self, fileToCheck=output_file)
        else:
            to_send = (
f"There was a problem with {self.show}.\n\n\
It looks like the source file doesn't exist. Please check manually! Yesterday's file will remain.\n\n\
{get_timestamp()}"
                )
            TLShow.send_notifications(self, message=to_send, subject='Error')
            print_to_screen_and_wait(message=to_send)
            raise FileNotFoundError
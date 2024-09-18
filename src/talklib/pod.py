from datetime import datetime
import xml.etree.ElementTree as ET
import glob
import os
from typing import Type

import boto3
from botocore.exceptions import ClientError
from pydantic import BaseModel, Field

from talklib.ev import EV
from talklib.notify import Notify
from talklib.ffmpeg import FFMPEG
from talklib.utils import raise_exception_and_wait, today_is_weekday

class AWS():
    ev = EV()
    bucket = 'tlpod'
    s3 = boto3.client(
    's3', 
    aws_access_key_id = ev.aws_access_key_id, 
    aws_secret_access_key = ev.aws_secret_access_key
    )

    def upload_file(self, bucket_folder, file):
        self.s3.upload_file(Bucket=self.bucket, Key=bucket_folder+'/'+file, Filename=file)

    def download_file(self, bucket_folder, file):
        self.s3.download_file(Bucket=self.bucket, Key=bucket_folder+'/'+file, Filename=file)
        return file

    def delete_file(self, bucket_folder, file):
        self.s3.delete_object(Bucket=self.bucket, Key=bucket_folder+'/'+file)
    
    def print_buckets(self):
    # Retrieve the list of existing buckets
        response = self.s3.list_buckets()
        response = response['Buckets']
        for bucket_name in response:
            return(bucket_name["Name"])

    def get_folders(self):
        folders = []
        result = self.s3.list_objects(Bucket=self.bucket)
        for contents in result["Contents"]:
            key:str = contents["Key"]
            if key.endswith("/"):
                folders.append(key.strip('/').lower())
        return folders
    
    def get_files(self):
        result = self.s3.list_objects(Bucket=self.bucket)
        for contents in result["Contents"]:
            key:str = contents["Key"]
            if not key.endswith("/"):
                print(key)

class Episode(BaseModel):
    feed_file: str 
    audio_filename: str
    bucket_folder: str
    episode_title: str

    pub_date: str = datetime.now().strftime('%a, %d %b %Y %H:%M:%S -5000')
    
    def size_in_bytes(self, filename):
        size_in_bytes = os.path.getsize(filename)
        size_in_bytes = str(size_in_bytes)
        return size_in_bytes
    
    def enclosure(self):
        enclosure = f"https://tlpod.s3.us-east-1.amazonaws.com/{self.bucket_folder}/{self.audio_filename}"
        return enclosure

    def add_new_episode(self):
        feed = ET.parse(self.feed_file)
        root = feed.getroot()
        root = root.find('channel')

        # make a new element, called 'item'
        item = ET.Element('item')

        # add elements to the item element
        title = ET.Element('title')
        title.text = self.episode_title
        item.append(title)

        pubDate = ET.Element('pubDate')
        pubDate.text = self.pub_date
        item.append(pubDate)

        enclosure = ET.Element('enclosure')
        enclosure.set('url', self.enclosure())
        enclosure.set('length', self.size_in_bytes(self.audio_filename))
        enclosure.set('type', 'audio/mpeg')
        item.append(enclosure)

        guid = ET.Element('guid')
        guid.set('isPermaLink', 'false')
        guid.text = self.audio_filename # this is just the name of the audio file. useful for deleting the file later on...
        item.append(guid)

        last_build_date = root.find('lastBuildDate')
        last_build_date.text = self.pub_date

        # insert the item element into the channel element, at index position x
        root.insert(10, item)

        ET.indent(feed) # makes the XML real pretty like
        feed.write(self.feed_file)
    
    def remove_old_episodes(self):
        feed = ET.parse(self.feed_file)
        root = feed.getroot()
        root = root.find('channel')
        number_of_items = root.findall('item')
        if len(number_of_items) > 10:
            guid_of_item = number_of_items[-1]
            guid = guid_of_item.find('guid').text
            root.remove(guid_of_item)
            AWS().delete_file(bucket_folder=self.bucket_folder, file=guid)
            ET.indent(feed)
            feed.write(self.feed_file)
        else:
            print('under 50')


class TLPod(BaseModel):
    '''
    everything should be in lower case!

    show: generic name for the show/program

    filename_to_match: the base name of the show we want to match. do not include the date.
    for example, to match RollingStone091322, use 'RollingStone'.

    bucket_folder: the name of the folder on S3 where the audio and RSS files are stored.
    should be lower case
    '''
    display_name: str
    filename_to_match: str
    bucket_folder: str
    audio_folders:list = EV().destinations
    notifications: Type[Notify] = Notify()
    ffmpeg: Type[FFMPEG] = FFMPEG()

    def match_file(self):
        '''match the name of the program that has today's date in the filename'''
        today_date: str = datetime.now().strftime("%m%d%y") # this is how we date our programs: MMDDYY
        to_match:str = self.filename_to_match + today_date
        self.__prep_syslog(message=f"looking for file to match: {to_match}")
        for dest in self.audio_folders:
            self.__prep_syslog(message=f"searching for {to_match} in {dest}...")
            files = glob.glob(f"{dest}/*.wav")
            for file in files:
                if to_match.lower() in file.lower():
                    self.__prep_syslog(message="found matching file!")
                    return file
        to_send = f"There was a problem podcasting {self.display_name}. Cannot find matched file {to_match} in {self.audio_folders}"
        raise Exception (to_send)
        # self.__send_notifications(message=to_send, subject='Error')
        # raise_exception_and_wait(message=to_send)

    def convert(self, file:str):
        self.__prep_syslog(message="Converting audio file to mp3...")
        a = FFMPEG()
        filename = file.split('.')
        filename = filename[0]
        filename = os.path.basename(filename).lower()
        a.input_file = file
        a.output_file = filename + '.mp3'
        ha = a.convert()
        self.__prep_syslog(message="File successfully converted")
        return ha
    
    def check_bucket_folder_exists(self):
        aws = AWS()
        folders = aws.get_folders()
        if self.bucket_folder.lower() in folders:
            return True
        return False



    def __prep_syslog(self, message: str, level: str = 'info'):
        '''send message to syslog server'''
        message = f'{self.display_name}: {message}'
        print(message)
        self.notifications.send_syslog(message=message, level=level)

    def __prep_send_mail(self, message: str, subject: str):
        '''send email to TL gmail account via relay address'''
        subject = f'{subject}: {self.display_name}'
        self.notifications.send_mail(subject=subject, message=message)

    def __send_sms_if_enabled(self, message: str):
        '''send sms via twilio IF twilio_enable is set to True'''
        self.notifications.send_sms(message=message)

    def __send_notifications(self, message: str, subject: str, syslog_level: str = 'error'):
        '''we generally only want to send SMS via Twilio if today is on a weekend'''
        if today_is_weekday():
            self.__prep_send_mail(message=message, subject=subject)
            self.__prep_syslog(message=message, level=syslog_level)
        else:
            self.__send_sms_if_enabled(message=message)
            self.__prep_send_mail(message=message, subject=subject)
            self.__prep_syslog(message=message, level=syslog_level)


    def run(self):
        self.__prep_syslog(message="Starting up...")
        audio_file = self.match_file()
        converted_file = self.convert(file=audio_file)

        if self.check_bucket_folder_exists():
            self.__prep_syslog(message=f"{self.bucket_folder} folder exists in bucket")
        else:
            to_send = f'cannot find bucket folder titled: {self.bucket_folder}.'
            self.__send_notifications(message=to_send, subject='Error')
            raise_exception_and_wait(message=to_send)

        aws = AWS()
        try:
            self.__prep_syslog(message=f"Downloading XML feed from {self.bucket_folder}")
            feed_file = aws.download_file(bucket_folder=self.bucket_folder, file='feed.xml')
        except ClientError as e:
            to_send = f'unable to download feed file: {e}'
            self.__send_notifications(message=to_send, subject='Error')
            raise_exception_and_wait(message=to_send)

        episode = Episode(
            feed_file=feed_file,
            audio_filename=converted_file,
            bucket_folder=self.bucket_folder,
            episode_title=f"{self.display_name} ({datetime.now().strftime('%a, %d %B')})"
            )
        self.__prep_syslog("adding episode to feed...")
        episode.add_new_episode()
        try:
            aws.upload_file(bucket_folder=self.bucket_folder, file=converted_file)
            aws.upload_file(bucket_folder=self.bucket_folder, file=feed_file)
        except ClientError as e:
            to_send = f'unable to download feed file: {e}'
            self.__send_notifications(message=to_send, subject='Error')
            raise_exception_and_wait(message=to_send)

        try:
            self.__prep_syslog(f"Deleting local file ({feed_file}) from {os.getcwd()}")
            os.remove(feed_file)
            self.__prep_syslog(f"Deleting local file ({converted_file}) from {os.getcwd()}")
            os.remove(converted_file)
        except:
            print('whoops')

        print('done?')
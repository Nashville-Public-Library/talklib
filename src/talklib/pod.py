from datetime import datetime
import glob
import os
from typing import Type

import boto3
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

    def delete_file(self, file):
        pass
    
    def print_buckets(self):
    # Retrieve the list of existing buckets
        response = self.s3.list_buckets()
        response = response['Buckets']
        for bucket_name in response:
            print(bucket_name["Name"])

    def print_folders(self):
        result = self.s3.list_objects(Bucket="tlpod")
        for contents in result["Contents"]:
            key:str = contents["Key"]
            if key.endswith("/"):
                print(key)
    
    def print_files(self):
        result = self.s3.list_objects(Bucket="tlpod")
        for contents in result["Contents"]:
            key:str = contents["Key"]
            if not key.endswith("/"):
                print(key)


class TLPod(BaseModel, AWS):
    '''
    show: generic name for the show/program

    filename_to_match: the base name of the show we want to match. do not include the date.
    for example, to match RollingStone091322, use 'RollingStone'.

    bucket_folder: the name of the folder on S3 where the audio and RSS files are stored.
    should be lower case
    '''
    show: str
    filename_to_match: str
    bucket_folder: str 
    audio_folders:list = EV().destinations
    notifications: Type[Notify] = Notify()
    ffmpeg: Type[FFMPEG] = FFMPEG()

    def match_file(self):
        '''match the name of the program that has today's date in the filename'''
        today_date: str = datetime.now().strftime("%m%d%y") # this is how we date our programs: MMDDYY
        to_match:str = self.filename_to_match + today_date
        for dest in self.audio_folders:
            files = glob.glob(f"{dest}/*.wav")
            for file in files:
                if to_match in file:
                    return os.path.basename(file)
        to_send = f"There was a problem podcasting {self.show}. Cannot find matched file {to_match} in {self.audio_folders}"
        raise Exception (to_send)
        # self.__send_notifications(message=to_send, subject='Error')
        # raise_exception_and_wait(message=to_send)

    def convert(self, file:str):
        a = FFMPEG()
        filename = file.split('.')
        filename = filename[0]
        a.input_file = file
        a.output_file = filename+'.mp3'
        ha = a.convert()
        return ha



    def __prep_syslog(self, message: str, level: str = 'info'):
        '''send message to syslog server'''
        message = f'{self.show}: {message}'
        print(message)
        self.notifications.send_syslog(message=message, level=level)

    def __prep_send_mail(self, message: str, subject: str):
        '''send email to TL gmail account via relay address'''
        subject = f'{subject}: {self.show}'
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
        audio_file = self.match_file()
        converted_file = self.convert(file=audio_file)
        aws = AWS()
        aws.upload_file(bucket_folder=self.bucket_folder, file=converted_file)
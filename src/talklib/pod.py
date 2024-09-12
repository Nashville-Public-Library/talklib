import boto3
import os
from typing import Type

from pydantic import BaseModel, Field

from talklib.ev import EV
from talklib.notify import Notify
from talklib.ffmpeg import FFMPEG

class AWS():
    s3 = boto3.client(
    's3', 
    aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"], 
    aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"]
    )
    
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


class TLPod(BaseModel):
    show: str = Field(default=None)
    show_filename: str = Field(default=None)
    bucket_folder: str = Field(default=None)
    notifications: Type[Notify] = Notify()
    ffmpeg: Type[FFMPEG] = FFMPEG()
    ev: Type[EV] = EV()
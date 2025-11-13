from datetime import datetime
import xml.etree.ElementTree as ET
import glob
import math
import os
import re
import subprocess
import time
from typing import ClassVar, Type

from fabric import Connection, Result
from paramiko.ssh_exception import SSHException as paramiko_SSH_exception
from pydantic import BaseModel, Field, model_validator
import requests

from talklib.ev import EV
from talklib.notify import Notify
from talklib.ffmpeg import FFMPEG
from talklib.utils import today_is_weekday

class Notifications(BaseModel):
    prefix: ClassVar[str] = None  # prefix all messages with identifier for the show/podcast
    notify: ClassVar[Type[Notify]] = Notify()

    def prep_syslog(self, message: str, level: str = 'info'):
        '''send message to syslog server'''
        message = f'{self.prefix}: {message}'
        print(message)
        self.notify.send_syslog(message=message, level=level)

    def prep_send_mail(self, message: str, subject: str):
        '''send email to TL gmail account via relay address'''
        subject = f'{subject}: {self.prefix}'
        self.notify.send_mail(subject=subject, message=message)

    def send_sms_if_enabled(self, message: str):
        '''send sms via twilio IF twilio_enable is set to True'''
        self.notify.send_sms(message=message)

    def send_notifications(self, message: str, subject: str, syslog_level: str = 'error'):
        '''we generally only want to send SMS via Twilio if today is on a weekend'''
        if today_is_weekday():
            self.prep_send_mail(message=message, subject=subject)
            self.prep_syslog(message=message, level=syslog_level)
        else:
            self.send_sms_if_enabled(message=self.prefix + ": " + message)
            self.prep_send_mail(message=message, subject=subject)
            self.prep_syslog(message=message, level=syslog_level)

class SSH(BaseModel):
    server: str = "assets.library.nashville.gov"
    user: str = EV().pod_server_uname
    connection: Type[Connection] = Connection(host=server, user=user)
    notifications: Notifications = Notifications()
    folder_exists: ClassVar[str] = False

    def upload_file(self, file: str, folder: str) -> None:
        self.check_folder_exists(folder=folder)
        
        try:
            self.notifications.prep_syslog(message=f"Attempting to upload '{file}' to {folder}/ on server")
            self.connection.put(local=file, remote=f"shows/{folder}", preserve_mode=False)
            self.notifications.prep_syslog(message=f"Successfully uploaded '{file}' to {folder}/ on server")
            return
        except (FileNotFoundError, Exception) as e:
            to_send = f"unable to upload '{file}': {e}"
            self.notifications.send_notifications(message=to_send, subject='Error')
            raise e

    def download_file(self, file: str, folder: str) -> None:
        folder = folder.lower()
        try:
            self.notifications.prep_syslog(message=f"Attempting to download '{file}' from {folder}/ on server")
            self.connection.get(remote=f"shows/{folder}/{file}")
            self.notifications.prep_syslog(message=f"Successfully downloaded '{file}' to {os.getcwd()}")
            return file
        except paramiko_SSH_exception as e:
            to_send = f"unable to download '{file}' due to an authentication error. Are your SSH keys correctly configured?\n\
The error from the SSH library is: {e}"
            self.notifications.send_notifications(message=to_send, subject='Error')
            raise e
        except FileNotFoundError as e:
            to_send = f"Unable to download {file} from /{folder}. It seems the file does not exist: {e}"
            self.notifications.send_notifications(message=to_send, subject='Error')
            raise e

    def delete_file(self, file: str, folder: str) -> None:
        try:
            self.notifications.prep_syslog(message=f"Attempting to delete '{file}' from {folder}/ on server")
            self.connection.sftp().remove(f"shows/{folder}/{file}")
            self.notifications.prep_syslog(message=f"Successfully deleted '{file}' from {folder}/ on server")
            return
        except (Exception, FileNotFoundError) as e:
            self.notifications.send_notifications(
                message=f"Unable to delete '{file}' from {folder}: {e}. Continuing automation...",
                subject="Error")
            
    def make_new_folder(self, folder: str) -> None:
        folder = folder.lower()
        if self.check_folder_exists_no_exception(folder=folder):
            raise Exception (f"{folder}/ already exists on server! Exiting...")
        self.connection.run(f"cd shows && mkdir {folder}", hide=True)
        self.notifications.prep_syslog(message=f"{folder}/ created on server")

    def get_folders(self) -> list:
        ret_val: list = []
        result: Result = self.connection.run("cd shows && ls", hide=True)
        result_stdout:str = result.stdout
        folders: list[str] = result_stdout.rsplit("\n")
        for folder in folders:
            if folder != "":
                ret_val.append(folder.lower())
        return ret_val
    
    def get_files_from_folder(self, folder: str) -> list:
        ret_val: list = []
        result: Result = self.connection.run(f"cd shows/{folder} && ls", hide=True)
        result_stdout:str = result.stdout
        files: list[str] = result_stdout.rsplit("\n")
        for file in files:
            if file != "": # exclude files without names?
                ret_val.append(file.lower())
        return ret_val
    
    def get_all_files(self) -> list:
        ret_val: list = []
        result: Result = self.connection.run("cd shows && ls -R", hide=True)
        result_stdout:str = result.stdout
        files: list[str] = result_stdout.rsplit("\n")
        for file in files:
            if not file.startswith("./") and file != "": # exclude folders and files without names
                ret_val.append(file.lower())
        return ret_val

    def get_feed_from_folder(self, folder: str):
        self.check_folder_exists(folder=folder)
        self.download_file(file="feed.xml", folder=folder)

    def upload_feed_to_folder(self, folder:str):
        self.upload_file(file="feed.xml", folder=folder)

    def check_folder_exists(self, folder: str) -> bool:
        if SSH.folder_exists:
            return True
        self.notifications.prep_syslog(message=f"checking if {folder}/ exists on server...")
        folders = self.get_folders()
        if folder.lower() in folders:
            self.notifications.prep_syslog(message=f"{folder}/ exists on server!")
            SSH.folder_exists = True
            return True
        
        to_send = f"cannot find folder titled: {folder}/ on server"
        self.notifications.send_notifications(message=to_send, subject='Error')
        raise Exception (to_send)
    
    def check_folder_exists_no_exception(self, folder: str):
        self.notifications.prep_syslog(message=f"checking if {folder}/ exists on server...")
        folders = self.get_folders()
        if folder.lower() in folders:
            self.notifications.prep_syslog(message=f"{folder}/ exists on server!")
            return True
    

class Episode(BaseModel):
    feed_file: str = Field(min_length=1, default=None)
    audio_filename: str = Field(min_length=1, default=None)
    bucket_folder: str = Field(min_length=1, default=None)
    episode_title: str = Field(min_length=1, default=None)
    notifications: Notifications = Notifications()
    max_episodes: int = Field(default=None)

    def pub_date(self) -> str: 
        timezone = time.timezone/60/60 # 60 seconds per minute, 60 minutes per hour
        timezone = round(timezone)  
        if time.localtime().tm_isdst: # if DST is currently active
            timezone-=1

        pub_date = datetime.now().strftime(f'%a, %d %b %Y %H:%M:%S -0{timezone}00')
        self.notifications.prep_syslog(message=f"pubDate will be: {pub_date}")
        return pub_date
    
    def copyright(self) -> str:
        year: int = datetime.now().year
        copyright: str = f"© 1975-{year} Nashville Talking Library - Do not copy or redistribute"
        self.notifications.prep_syslog(message=f"copyright will be: {copyright}")
        return copyright
    
    def size_in_bytes(self, filename) -> str:
        size_in_bytes = os.path.getsize(filename)
        size_in_bytes = str(size_in_bytes)
        self.notifications.prep_syslog(message=f"enclosure lenth will be {size_in_bytes}")
        return size_in_bytes
    
    def enclosure(self) -> str:
        enclosure = f"https://dts.podtrac.com/redirect.mp3/assets.library.nashville.gov/talkinglibrary/shows/{self.bucket_folder}/{self.audio_filename}"
        self.notifications.prep_syslog(message=f"enclosure will be {enclosure}")
        return enclosure
    
    def itunes_duration(self) -> str:
        ffmpeg = FFMPEG(input_file=self.audio_filename)
        duration = ffmpeg.get_length_in_minutes()
        seconds, minutes = math.modf(duration)

        minutes = round(minutes)

        seconds = seconds*60
        seconds = round(seconds)

        result = f"{minutes}:{seconds:02}"
        self.notifications.prep_syslog(message=f"itunes:duration will be {result}")
        return result
    
    def get_root_feed_file(self):
        ET.register_namespace(prefix="atom", uri="http://www.w3.org/2005/Atom")
        ET.register_namespace(prefix="itunes", uri="http://www.itunes.com/dtds/podcast-1.0.dtd")
        feed = ET.parse(self.feed_file)
        root = feed.getroot()
        return root

    
    def check_for_duplicate_episode(self):
        self.notifications.prep_syslog(message="checking for duplicate episode...")
        root = self.get_root_feed_file()
        channel = root.find("channel")
        items = channel.findall("item")
        for item in items:
            item = item.find("title").text
            if item == self.episode_title:
                to_send = "Found episode with identical title already in feed. Aborting..."
                self.notifications.send_notifications(message=to_send, subject="Error")
                self.cleanup_files_on_abort()
                raise Exception (to_send)
        self.notifications.prep_syslog(message="no duplicate episode found")
        return
    
    def cleanup_files_on_abort(self):
        self.notifications.prep_syslog(message=f"Aborting automation, deleting local temp files...")
        files = glob.glob("*.mp3")
        for file in files:
            self.notifications.prep_syslog(message=f"Attempting to delete: {file}")
            try:
                os.remove(file)
                self.notifications.prep_syslog(message=f"Successfully deleted: {file}")
            except:
                self.notifications.prep_syslog(message=f"Unable to delete {file}")

        self.notifications.prep_syslog(message=f"Attempting to delete: feed.xml")
        try:          
            os.remove("feed.xml")
            self.notifications.prep_syslog(message=f"Successfully deleted: feed.xml")
        except:
            self.notifications.prep_syslog(message=f"Unable to delete:: feed.xml")

    def add_new_episode(self):
        '''Create an 'item' element. Then create all of the necessary sub elements and append them to the item element'''
        ET.register_namespace(prefix="atom", uri="http://www.w3.org/2005/Atom")
        ET.register_namespace(prefix="itunes", uri="http://www.itunes.com/dtds/podcast-1.0.dtd")
        feed = ET.parse(self.feed_file)
        root = feed.getroot()
        root = root.find('channel')

        # if we have a new feed, or a feed with no episodes
        self.check_for_duplicate_episode()

        self.notifications.prep_syslog(message="Building the new <item> element")
        item = ET.Element('item')

        title = ET.Element('title')
        title.text = self.episode_title
        item.append(title)

        # Drupal needs to see a category element on every episode that matches the name of the program
        channel_title_category_element = ET.Element("category")
        channel_title_category_element.text = root.find('title').text
        item.append(channel_title_category_element)

        pubDate = ET.Element('pubDate')
        pubDate.text = self.pub_date()
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

        itunes_duration_element = ET.Element("itunes:duration")
        itunes_duration_element.text = self.itunes_duration()
        item.append(itunes_duration_element)

        # insert the new 'item' element as the first item, but below all the other channel elements
        items = root.findall('item')
        if items:
            # If there are existing items (there usually will be), add the new item before to the top
            first_item = items[0]
            index = list(root).index(first_item)
            self.notifications.prep_syslog(message=f"adding {item} to feed at channel index: {index}")
            root.insert(index, item)
        else:
            # If no items exist, add the new item to the bottom (after the other channel elements)
            root.append(item)

        last_build_date = root.find('lastBuildDate')
        last_build_date.text = self.pub_date() # fine to use this same pub date, as the format for both is the same

        copyright = root.find("copyright")
        copyright.text = self.copyright()

        ET.indent(feed) # makes the XML pretty looking
        self.notifications.prep_syslog(message=f"writing feed file...")
        feed.write(self.feed_file, encoding="utf-8", xml_declaration=True)
    
    def remove_old_episodes(self):
        ET.register_namespace(prefix="atom", uri="http://www.w3.org/2005/Atom")
        ET.register_namespace(prefix="itunes", uri="http://www.itunes.com/dtds/podcast-1.0.dtd")
        feed = ET.parse(self.feed_file)
        root = feed.getroot()
        root = root.find('channel')
        items = root.findall('item')
        number_of_items = len(items)
        index = -1
        while number_of_items > self.max_episodes:
            self.notifications.prep_syslog(message=f"There are currently {number_of_items} items in the feed, which is above {self.max_episodes}")
            item_to_remove = items[index] # locate last item in feed
            guid = item_to_remove.find('guid').text # grab the guid (filename) so we can delete the file from the server
            self.notifications.prep_syslog(f'removing from feed: {item_to_remove}')
            root.remove(item_to_remove)
            
            SSH().delete_file(folder=self.bucket_folder, file=guid)
            
            ET.indent(feed)
            self.notifications.prep_syslog(message=f"writing to feed file...")
            feed.write(self.feed_file, encoding="utf-8", xml_declaration=True)
            number_of_items-=1
            index-=1 


class TLPod(BaseModel):
    '''
    everything should be in lower case!

    display_name: generic name for the show/program. WIll be displayed as the
    episode "Title" in the podcast feed. type=string

    filename_to_match: the base name of the show we want to match. do not include the date.
    for example, to match RollingStone091322, use 'RollingStone'. type=string

    bucket_folder: the name of the folder on S3 where the audio and RSS files are stored.
    should be lower case. type=string

    max_episodes_in_feed: the max number of episodes that should be in the feed after you add the episode.
    '''
    display_name: str = Field(min_length=1)
    filename_to_match: str = Field(min_length=1)
    bucket_folder: str = Field(default=None)
    max_episodes_in_feed: int = Field(ge=1, default=5)
    override_filename: bool = False
    short_timestamp: bool = False
    preroll: bool = True
    audio_folders:list = EV().destinations
    notifications: Type[Notifications] = Notifications()
    episode: Type[Episode] = Episode()
    ffmpeg: Type[FFMPEG] = FFMPEG()
    ssh: Type[SSH] = SSH()

    @model_validator(mode='after')
    def post_update(self):
        '''
        the name of the bucket folder should match the base name of the file. If bucket_folder is not explicitly set
        by the user, use the filename. However, if filename_override is being used, strip out the digits first.
        '''
        if not self.bucket_folder:
            if self.override_filename:
                self.bucket_folder = re.sub(pattern="[0-9]", string=self.filename_to_match.lower(), repl='')
            else: 
                self.bucket_folder = self.filename_to_match.lower()

        prefix = f"{self.display_name} (podcast)"
        Notifications.prefix = prefix

        if self.short_timestamp:
            self.display_name = f"{self.display_name} ({self.short_timestamp_for_display_name()})"
        else:
            self.display_name = f"{self.display_name} ({datetime.now().strftime('%a, %d %b')})"

        return self
    
    # @model_validator(mode='after')
    # def confirm_SSH_connection(self):
    #     # before we carry on, make sure we can successfully connect to the server
    #     try:
    #         connection = self.ssh.connection.run("ls")
    #     except Exception as e:
    #         to_send:str = f"Cannot connect to server. Are you sure the SSH keys are set up correctly? Here is the error: {e}"
    #         self.notifications.send_notifications(message=to_send, subject="Error")
    #         raise e

    #     return self
    def short_timestamp_for_display_name(self):
            day_of_week: str = datetime.now().strftime("%A") # Weekday as locale’s full name.
            hour: str = datetime.now().strftime('%I') # Hour (12-hour clock) as a zero-padded decimal number.
            ampm: str = datetime.now().strftime("%p") # Locale’s equivalent of either AM or PM.

            if hour == "00":
                hour = "12"

            return f"{day_of_week} {hour}{ampm}"
    
    def get_filename_to_match(self) -> str:
        if self.override_filename:
            self.notifications.prep_syslog(message="filename override is turned ON")
            file = (self.filename_to_match).lower()
            return file
        today_date: str = datetime.now().strftime("%m%d%y") # this is how we date our programs: MMDDYY
        return (self.filename_to_match + today_date).lower()

    def check_alt_endings(self,file: str):
        file_lower_case: str = file.lower()
        
        if file_lower_case.endswith("-sub.wav"):
            self.notifications.prep_syslog(message=f"'-sub' found in filename: {file}. Amending 'display_name' for episode...")
            self.display_name = f"{self.display_name} (Substitute)"
            self.notifications.prep_syslog(message=f"New display_name: {self.display_name}")

        if file_lower_case.endswith("-rep.wav"):
            self.notifications.prep_syslog(message=f"'-rep' found in filename: {file}. Amending 'display_name' for episode...")
            self.display_name = f"{self.display_name} (Encore)"
            self.notifications.prep_syslog(message=f"New display_name: {self.display_name}")
        
        if file_lower_case.endswith("-dnp.wav"):
            to_send = f"'-dnp' found in filename ({file}), will NOT podcast this episode. Exiting automation!"
            self.notifications.send_notifications(message=to_send, subject="Info", syslog_level="info")
            raise Exception (to_send)

    def match_file(self):
        '''match the name of the program that has today's date in the filename'''
        to_match = self.get_filename_to_match()
        self.notifications.prep_syslog(message=f"looking for file to match: {to_match}")
        for dest in self.audio_folders:
            self.notifications.prep_syslog(message=f"searching for {to_match} in {dest}...")
            files = glob.glob(f"{dest}/*.wav")
            for file in files:
                if to_match in file.lower():
                    self.notifications.prep_syslog(message=f"found matching file: {file}")

                    if "Copy (" in file:
                        self.notifications.prep_syslog(message=f"skipping file with 'copy' in filename: {file}")
                        continue

                    self.check_alt_endings(file=file)
                    
                    return file
                
        to_send = f"There was a problem podcasting {self.display_name}. Cannot find matched file {to_match} in {self.audio_folders}"
        self.notifications.send_notifications(message=to_send, subject='Error')
        raise FileNotFoundError
    
    def create_converted_filename(self, file: str):
        output_filename = file.split('.')
        output_filename = output_filename[0]
        output_filename = os.path.basename(output_filename).lower()
        output_filename = output_filename + '.mp3'
        self.notifications.prep_syslog(message=f"final audio file will be {output_filename}")
        return output_filename

    def convert(self, file:str):
        self.ffmpeg.input_file = file
        self.ffmpeg.output_file = "out.mp3"
        self.ffmpeg.compression = False # this is for podcasts. these files should already be edited  
        
        ffmpeg_commands = self.ffmpeg.get_commands()
        self.notifications.prep_syslog(message=f"FFmppeg commands: {ffmpeg_commands}")

        self.notifications.prep_syslog(message=f"Converting {file} to mp3...")
        try:
            output = self.ffmpeg.convert()
            self.notifications.prep_syslog(message="File successfully converted")
            return output
        except Exception as ffmpeg_exception:
            self.notifications.send_notifications(message=f'FFmpeg error: {ffmpeg_exception}', subject='Error')
            raise ffmpeg_exception
        
    def concat(self, preroll:str, program_audio: str, output_filename: str):
        if not self.preroll:
            os.rename(program_audio, output_filename)
            return output_filename
        self.notifications.prep_syslog(message="concatenating preroll and program audio together...")
        subprocess.run(f'ffmpeg -hide_banner -loglevel quiet -i "concat:{preroll}|{program_audio}" -c copy {output_filename}')
        self.notifications.prep_syslog(message=f"files successfully concatenated as: {output_filename}")
        return output_filename

    def download_preroll(self):
        download_URL = "https://assets.library.nashville.gov/talkinglibrary/pod_preroll.mp3"
        input_file = 'preroll.mp3'
        self.notifications.prep_syslog(message=f"Attempting to download preroll audio from {download_URL}...")
        with open (input_file, mode='wb') as downloaded_file:
            try:
                a = requests.get(download_URL)
                downloaded_file.write(a.content)
                downloaded_file.close()
            except (Exception, requests.exceptions.RequestException) as e:
                self.notifications.send_notifications(message=f"Cannot download {download_URL}. Exception: {e}", subject="Error")
                raise e
        self.notifications.prep_syslog(message="preroll audio successfully downloaded")
        return downloaded_file.name
    
    def post_cleaup(self):
        self.notifications.prep_syslog(message="looking for local files to delete...")
        XML_files = glob.glob("*.xml")
        for file in XML_files:
            self.delete_local_file(file=file)
        MP3_files = glob.glob("*.mp3")
        for file in MP3_files:
            self.delete_local_file(file=file)
    
    def delete_local_file(self, file: str):
        try:
            self.notifications.prep_syslog(message=f"Attempting to delete local file: {file}")
            os.remove(file)
            self.notifications.prep_syslog(message=f"Successfully deleted local file: {file}")
            return
        except Exception:
            self.notifications.prep_syslog(message=f"Unable to delete local file: {file}")

    def run(self):
        self.notifications.prep_syslog(message="Starting up...")
        self.notifications.prep_syslog(message=f"Attributes: {self.__repr__()}")

        self.ssh.check_folder_exists(folder=self.bucket_folder)

        audio_file = self.match_file()
        converted_file = self.convert(file=audio_file)
        output_filename = self.create_converted_filename(file=audio_file)
        preroll = self.download_preroll()
        concat_file = self.concat(preroll=preroll, program_audio=converted_file, output_filename=output_filename)

        feed_file = self.ssh.download_file(folder=self.bucket_folder, file='feed.xml') # all XML files on server should have the same name

        self.episode.feed_file = feed_file
        self.episode.audio_filename = concat_file
        self.episode.bucket_folder = self.bucket_folder
        self.episode.episode_title = self.display_name
        self.episode.max_episodes = self.max_episodes_in_feed
       
        self.episode.add_new_episode()
        self.episode.remove_old_episodes()
    
        self.ssh.upload_file(folder=self.bucket_folder, file=concat_file)
        self.ssh.upload_file(folder=self.bucket_folder, file=feed_file)

        self.post_cleaup()

        self.notifications.prep_syslog(message="All done.")
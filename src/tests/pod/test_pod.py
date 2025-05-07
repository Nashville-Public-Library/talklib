import atexit
from datetime import datetime
import glob
import os
import shutil

from pydantic_core import ValidationError
import pytest

from talklib.pod import TLPod, Episode
from .mock import mock_destinations, download_test_file, write_mock_feed, write_mock_feed_no_items


def test_type_1():
    '''pydantic should raise an error if instance variables aren't set'''
    with pytest.raises(ValidationError):
            test = TLPod()

def test_type_2():
    '''pydantic should raise an error if wrong type passed in'''
    with pytest.raises(ValidationError):
            test = TLPod(
                display_name=5, 
                filename_to_match="del")
            
def test_type_3():
    '''pydantic should raise an error if wrong type passed in'''
    with pytest.raises(ValidationError):
            test = TLPod(
                display_name='Some Name', 
                filename_to_match=5)

def test_type_4():
    '''pydantic should raise an error if wrong type passed in'''
    with pytest.raises(ValidationError):
            test = TLPod(
                display_name='delete', 
                filename_to_match="del",
                bucket_folder=5)
            
def test_type_5():
    '''pydantic should raise an error if wrong type passed in'''
    with pytest.raises(ValidationError):
            test = TLPod(
                display_name='delete', 
                filename_to_match="del",
                max_episodes_in_feed=3.1)
            
def test_type_6():
    '''pydantic should raise an error if wrong type passed in'''
    with pytest.raises(ValidationError):
            test = TLPod(
                display_name='delete', 
                filename_to_match="del",
                override_filename=5)
            
def test_type_7():
    '''pydantic should raise an error if wrong type passed in'''
    with pytest.raises(AttributeError):
            test = TLPod(
                display_name='delete', 
                filename_to_match="del",
                )
            test.notifications.prefix = 3 # must be a string

def test_notif_prefix():
      '''notification prefix should be set to include the display name'''
      test = TLPod(
            display_name="mahhh",
            filename_to_match='mah'
      )
      assert "mahhh" in test.notifications.prefix
            
def test_bucket_filename_match():
          '''if no bucket folder is set explicitly, bucket folder should be set to filename_to_match'''
          test = TLPod(
               display_name='testing',
               filename_to_match = 'testing123'
          )
          assert test.bucket_folder == test.filename_to_match
            
# def test_match_file_1():
#     '''checking matched filename'''
#     test = TLPod(
#         display_name = 'test',
#         filename_to_match='test',
#         bucket_folder='test'
#       )
#     test.notifications.enable_all = False
#     today = datetime.now().strftime("%m%d%y")
#     test_file = download_test_file(filename=f'test{today}.mp3')
#     for dest in test.audio_folders:
#         shutil.copy(test_file, dest)

#     assert type(test.match_file()) == str

def test_match_file_2():
    '''should raise exception if matching filename cannot be found'''
    test = TLPod(
        display_name='test',
        filename_to_match='notExist',
        bucket_folder='nope'
    )
    test.notifications.notify.enable_all = False
    with pytest.raises(FileNotFoundError):
        test.match_file()

def test_match_bucket_folder_1():
    '''should raise exception if matching bucket folder cannot be found'''
    test = TLPod(
        display_name='test',
        filename_to_match='notExist',
        bucket_folder='doesNotExist'
    )
    test.notifications.notify.enable_all = False
    with pytest.raises(Exception):
        test.run()

def test_check_for_duplicate_episode_1():
    '''if a matching title is found in episode list, an exception should be raised'''
    ep = Episode(
            feed_file=write_mock_feed(),
            audio_filename=download_test_file(),
            bucket_folder="none",
            episode_title="Mock Title 011525"
      )
    ep.notifications.notify.enable_all = False
    with pytest.raises(Exception):
        ep.check_for_duplicate_episode()

def test_check_for_duplicate_episode_2():
    '''no exception if matching title is not found'''
    ep = Episode(
            feed_file=write_mock_feed(),
            audio_filename=download_test_file(),
            bucket_folder="none",
            episode_title="Not A Duplicate Title"
      )
    ep.notifications.notify.enable_all = False
    ep.check_for_duplicate_episode()

def test_check_for_duplicate_episode_3():
    '''no exception even if there are no items in the feed'''
    ep = Episode(
            feed_file=write_mock_feed_no_items(),
            audio_filename=download_test_file(),
            bucket_folder="none",
            episode_title="Not A Duplicate Title"
      )
    ep.notifications.notify.enable_all = False
    ep.check_for_duplicate_episode()

# XML/EPISODE STUFF

def test_pub_date_1():
     '''formatted as a string'''
     episode = Episode()
     pub_date = episode.pub_date()
     assert type(pub_date) == str

def test_pub_date_2():
     '''should have today's date info in it'''
     episode = Episode()
     day = datetime.now().strftime("%a")
     month = datetime.now().strftime("%b")
     year = datetime.now().strftime("%Y")
     pub_date = episode.pub_date()
     assert day in pub_date
     assert month in pub_date
     assert year in pub_date

def test_copyright_1():
     '''formatted as a string'''
     episode = Episode()
     copyright= episode.copyright()
     assert type(copyright) == str

def test_copyright_2():
     '''current year should be in string'''
     episode = Episode()
     year = datetime.now().year
     year = str(year)
     copyright = episode.copyright()
     assert year in copyright




def teardown():
    """remove temp files/folders that were created for the tests"""
    files = glob.glob("*.wav") + glob.glob("*.mp3") + glob.glob("*.xml")
    for file in files:
         os.remove(file)
         print("removed" + file)
    
    shutil.rmtree(mock_destinations())

atexit.register(teardown)
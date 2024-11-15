import atexit
from datetime import datetime
import os
import shutil
from unittest.mock import patch

from pydantic_core import ValidationError
import pytest

from .mock import env_vars, mock_destinations, download_test_file
with patch.dict('os.environ', env_vars):
        from talklib.pod import TLPod


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
                filename_override=5)
            
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

def teardown():
    today = datetime.now().strftime("%m%d%y")

    today = f'test{today}.wav'
    try:
        os.remove(today)
        shutil.rmtree(mock_destinations())
    except:
         pass
        

atexit.register(teardown)
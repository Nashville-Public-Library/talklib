import atexit
from datetime import datetime
import os
import shutil
from unittest.mock import patch

from pydantic_core import ValidationError
import pytest

from .mock import env_vars, mock_destinations, download_test_file
with patch.dict('os.environ', env_vars):
    from talklib import TLPod
    from talklib.pod import AWS



def test_type_1():
    '''pydantic should raise an error if wrong type passed in'''
    with pytest.raises(ValidationError):
            test = TLPod(
                display_name=5, 
                show_filename="del",
                bucket_folder='nope')
            
def test_type_2():
    '''pydantic should raise an error if wrong type passed in'''
    with pytest.raises(ValidationError):
            test = TLPod(
                display_name=5, 
                show_filename=5,
                bucket_folder='nope')

def test_type_3():
    '''pydantic should raise an error if wrong type passed in'''
    with pytest.raises(ValidationError):
            test = TLPod(
                display_name='delete', 
                show_filename="del",
                bucket_folder=5)
            
def test_match_file_1():
    '''checking matched filename'''
    test = TLPod(
        display_name = 'test',
        filename_to_match='test',
        bucket_folder='test',
      )
    today = datetime.now().strftime("%m%d%y")
    test_file = download_test_file(filename=f'test{today}.wav')
    for dest in test.audio_folders:
        shutil.copy(test_file, dest)

    assert type(test.match_file()) == str

@patch('builtins.input', side_effect=['11', '13', 'Bob'])
def test_match_file_2(self):
    '''should raise exception if invalid filename passed in'''
    test = TLPod(
        display_name='test',
        filename_to_match='notExist',
        bucket_folder='nope'
    )
    test.notifications = False
    with pytest.raises(Exception):
        test.match_file()
            
# def test_buckets():
#     a = AWS()
#     a.print_buckets()
#     a.print_folders()
#     a.print_files()

def teardown():
    today = datetime.now().strftime("%m%d%y")

    today = f'test{today}.wav'
    try:
        os.remove(today)
        shutil.rmtree(mock_destinations())
    except:
         pass
        

atexit.register(teardown)
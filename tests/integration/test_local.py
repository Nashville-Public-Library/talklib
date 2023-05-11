import pytest
import requests
from unittest.mock import patch
import os
import shutil

from ...show import TLShow
from . import mock

url = 'https://pnsne.ws/3mVuTax'
input_file = 'input.mp3'  # name the file we download

@pytest.fixture
def template():
    test = TLShow()
    test.show = 'Delete Me'
    test.show_filename = 'delete_me'
    test.local_file = download_test_file()
    test.is_local = True

    test.destinations = mock.mock_destinations()

    # disable notifications for testing. Need separate tests for these!
    test.notifications = False
    test.syslog_enable = False

    yield test
    
    mock.remove_destinations()

    test.remove_yesterday = True
    test.remove_yesterday_files()

    # if you try and don't succeed...
    try:
        os.remove(input_file)
    except:
        # ...life goes on
        pass

def download_test_file():
    with open (input_file, mode='wb') as downloaded_file:
        a = requests.get(url)
        downloaded_file.write(a.content)
        downloaded_file.close()
    return downloaded_file.name

# ---------- full run ---------- # 

def test_run(template: TLShow):
    '''asserts no exception is raised for normal/correct case'''
    template.run()


def test_run_no_file(template: TLShow):
    '''check exception is raised with incorrect file name/path'''
    template.local_file = 'nofile'
    with pytest.raises(FileNotFoundError):
        template.run()
 
def test_run_no_URL_OR_local(template: TLShow):
    '''should raise an exception if neither URL NOR local is declared'''
    template.url = None
    template.is_local = None
    with pytest.raises(Exception):
        template.run()

def test_run_remove_source(template: TLShow):
    '''source file should be removed if this attribute is declared'''
    template.remove_source = True
    template.run()
    assert os.path.exists(input_file) == False

def test_check_length(template: TLShow):
    ''''''
    template.check_if_above = 10
    template.check_if_below = 5
    assert type(template.check_length(fileToCheck=template.local_file)) == float
    

'''
We are doing this because the print_to_screen function is called which calls the builtin 'input' function.
Thus pytest will complain since it needs to read standard out while running the tests, but in the process
our code is calling for input. It confuses the test, so we need to mock giving the program some input
when called for it. This is ugly and I'm sorry, but I do not want to lose the input function,
since it is a needed reminder to the user that something bad has happened!
'''
@patch('builtins.input', side_effect=['11', '13', 'Bob'])
def test_run_none_file(self, template: TLShow):
    template.local_file = None
    with pytest.raises(FileNotFoundError):
        template.run()
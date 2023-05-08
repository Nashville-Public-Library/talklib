import pytest
import requests
from unittest import mock
import os

from talklib.show import TLShow

url = 'https://pnsne.ws/3mVuTax'
input_file = 'input.mp3'  # name the file we download

@pytest.fixture
def template():
    test = TLShow()
    test.show = 'Delete Me'
    test.show_filename = 'delete_me'
    test.local_file = download_test_file()
    test.is_local = True
    # disable notifications for testing. Need separate tests for these!
    test.notifications = False
    test.syslog_enable = False

    return test

def download_test_file():
    with open (input_file, mode='wb') as downloaded_file:
        a = requests.get(url)
        downloaded_file.write(a.content)
        downloaded_file.close()
    return downloaded_file.name

# ---------- full run ---------- # 

def test_run(template):
    '''asserts no exception is raised for normal/correct case'''
    template.run()


def test_run_1a(template):
    '''check exception is raised with incorrect file name/path'''
    template.local_file = 'nofile'
    with pytest.raises(FileNotFoundError):
        template.run()
 
def test_run_2(template):
    
    template.url = None
    template.is_local = None
    with pytest.raises(Exception):
        template.run()

def test_check_length(template):
    
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
@mock.patch('builtins.input', side_effect=['11', '13', 'Bob'])
def test_run_3(self, template):
    template.local_file = None
    with pytest.raises(FileNotFoundError):
        template.run()

# ---------- Teardown/Cleanup ----------

def test_teardown(template):
    '''don't forget to delete the audio'''
    template.remove_yesterday = True
    template.remove_yesterday_files()
    os.remove(input_file)

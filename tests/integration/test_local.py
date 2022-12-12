import pytest
from unittest import mock
import os

from ...show import TLShow

url = 'https://pnsne.ws/3mVuTax'
cwd = os.getcwd()

def generate_test_instance():
    test = TLShow()
    test.show = 'Delete Me'
    test.show_filename = 'delete_me'
    
    # this is ugly. i am sorry
    if 'tests' in cwd:
        test.local_file = 'local_test_file.mp3'
    else: 
        test.local_file = 'tests/local_test_file.mp3'

    test.is_local = True
    # disable notifications for testing. Need separate tests for these!
    test.notifications = False
    test.syslog_enable = False

    return test

# ---------- full run ---------- # 

def test_run():
    '''asserts no exception is raised for normal/correct case'''
    test = generate_test_instance()
    test.run()


def test_run_1a():
    '''check exception is raised with incorrect file name/path'''
    test = generate_test_instance()
    test.local_file = 'nofile'
    with pytest.raises(FileNotFoundError):
        test.run()
 
def test_run_2():
    test = generate_test_instance()
    test.url = None
    test.is_local = None
    with pytest.raises(Exception):
        test.run()

'''
We are doing this because the print_to_screen function is called which calls the builtin 'input' function.
Thus pytest will complain since it needs to read standard out while running the tests, but in the process
our code is calling for input. It confuses the test, so we need to mock giving the program some input
when called for it. This is ugly and I'm sorry, but I do not want to lose the input function,
since it is a needed reminder to the user that something bad has happened!
'''
@mock.patch('builtins.input', side_effect=['11', '13', 'Bob'])
def test_run_3(self):
    test = generate_test_instance()
    test.local_file = None
    with pytest.raises(FileNotFoundError):
        test.run()

# ---------- Teardown/Cleanup ----------

def test_teardown():
    '''don't forget to delete the audio'''
    test = generate_test_instance()
    test.remove_yesterday = True
    test.remove_yesterday_files()

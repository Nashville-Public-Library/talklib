import pytest

from ...show import TLShow

url = 'https://pnsne.ws/3mVuTax'

def generate_test_instance():
    test = TLShow()
    test.show = 'Delete Me'
    test.show_filename = 'delete_me'
    test.url = url
    test.is_permalink = True
    # disable notifications for testing. Need separate tests for these!
    test.notifications = False
    test.syslog_enable = False
    return test

# ---------- full run ---------- # 

def test_run():
    '''asserts no exceptions are raised for the correct/normal case'''
    test = generate_test_instance()
    test.run()

def test_run2():
    '''asserts an exception is raised with an invalid url'''
    test = generate_test_instance()
    test.url = 'nourl'
    with pytest.raises(Exception):
        test.run()

# ---------- Teardown/Cleanup ----------

def test_teardown():
    '''don't forget to delete the audio'''
    test = generate_test_instance()
    test.remove_yesterday = True
    test.remove_yesterday_files()
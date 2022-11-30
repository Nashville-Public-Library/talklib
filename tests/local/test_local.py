import pytest

from ...show import TLShow

url = 'https://pnsne.ws/3mVuTax'

def generate_test_instance():
    test = TLShow()
    test.show = 'Delete Me'
    test.show_filename = 'delete_me'
    test.local_file = 'audio/local_test_file.mp3'
    test.is_local = True
    # disable notifications for testing. Need separate tests for these!
    test.notifications = False
    test.syslog_enable = False
    return test

# ---------- full run ---------- # 

def test_run():
    '''asserts no exception is raised for normal/correct case'''
    test = generate_test_instance()
    with pytest.raises(Exception):
        assert test.run()

def test_run2():
    '''check exception is raised with incorrect file name/path'''
    test = generate_test_instance()
    test.local_file = 'nofile'
    with pytest.raises(Exception):
        test.run()

# ---------- Teardown/Cleanup ----------

def test_teardown():
    '''don't forget to delete the audio'''
    test = generate_test_instance()
    test.remove_yesterday = True
    test.removeYesterdayFiles()
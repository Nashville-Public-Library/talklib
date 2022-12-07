'''
getting started with some general tests for the talklib module via Pytest.
'''
import pytest

from ...show import TLShow
import xml.etree.ElementTree as ET


# this RSS feed chosen as test feed because it is reliably updated every day 
# (many times per day) and because the audio file is short/small!
url = 'https://feeds.npr.org/500005/podcast.xml'

def generate_test_instance():
    test = TLShow()
    test.show = 'Delete Me'
    test.show_filename = 'delete_me'
    test.url = url
    # disable notifications for testing. Need separate tests for these!
    test.notifications = False
    test.syslog_enable = False
    return test

# ---------- run ----------
        
def test_run():
    '''implementation test with real audio. asserts that no exceptions are raised'''
    test = generate_test_instance()
    test.run()

def test_run2():
    test = generate_test_instance()
    test.url = 'invalid_URL'
    with pytest.raises(Exception):
        test.run()

# ---------- Teardown/Cleanup ----------

def test_teardown():
    '''don't forget to delete the audio'''
    test = generate_test_instance()
    test.remove_yesterday = True
    test.removeYesterdayFiles()

'''
getting started with some general tests for the talklib module via Pytest.
'''
import pytest

from ...show import TLShow
import xml.etree.ElementTree as ET


# this RSS feed chosen as test feed because it is reliably updated every day 
# (many times per day) and because the audio file is short/small!
url = 'https://feeds.npr.org/500005/podcast.xml'

@pytest.fixture(scope='module', autouse=True)
def template():
    test = TLShow()
    test.show = 'Delete Me'
    test.show_filename = 'delete_me'
    test.url = url
    # disable notifications for testing. Need separate tests for these!
    test.notifications = False
    test.syslog_enable = False
    
    return test

# ---------- run ----------
        
def test_run(template):
    '''implementation test with real audio. asserts that no exceptions are raised'''
    template.run()

def test_run2(template):
    template.url = 'invalid_URL'
    with pytest.raises(Exception):
        template.run()

def test_run3(template):
    '''assert an exception is raised when the URL is a valid URL but not an rss feed'''
    template.url = 'https://pnsne.ws/3mVuTax'
    with pytest.raises(Exception):
        template.run()

# ---------- Teardown/Cleanup ----------

def test_teardown(template):
    '''don't forget to delete the audio'''
    template.remove_yesterday = True
    template.remove_yesterday_files()

'''
getting started with some general tests for the talklib module via Pytest.
'''
import pytest

try:
    from ...show import TLShow
except KeyError:
    pass
from . import mock

# this RSS feed chosen as test feed because it is reliably updated every day 
# (many times per day) and because the audio file is short/small!

url = 'https://feeds.npr.org/500005/podcast.xml'

@pytest.fixture()
def template():
    test = TLShow()
    test.show = 'Delete Me'
    test.show_filename = 'delete_me'
    test.url = url

    test.destinations = mock.mock_destinations()

    # disable notifications for testing. Need separate tests for these!
    test.notifications = False
    test.syslog_enable = False
    
    yield test

    mock.remove_destinations()

# ---------- run ----------
        
def test_run(template: TLShow):
    '''implementation test with real audio. asserts that no exceptions are raised'''
    template.run()

def test_run2(template: TLShow):
    template.url = 'invalid_URL'
    with pytest.raises(Exception):
        template.run()

def test_run3(template: TLShow):
    '''assert an exception is raised when the URL is a valid URL but not an rss feed'''
    template.url = 'https://pnsne.ws/3mVuTax'
    with pytest.raises(Exception):
        template.run()

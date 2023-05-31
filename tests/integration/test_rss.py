'''
getting started with some general tests for the talklib module via Pytest.
'''
import pytest
from unittest.mock import patch

from ...show import TLShow
from .. import mock
from ..mock import env_vars

# this RSS feed chosen as test feed because it is reliably updated every day 
# (many times per day) and because the audio file is short/small!

url = 'https://feeds.npr.org/500005/podcast.xml'

@pytest.fixture()
def template():
    with patch.dict('os.environ', env_vars):
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

def test_run_bad_feed(template: TLShow):
    '''asserts an exception is raised for a non-updated feed'''
    bad_feed = 'https://www.pythonpodcast.com/rss' # hasn't been updated in a while.
    template.url = bad_feed
    with pytest.raises(Exception):
        with patch('builtins.input', return_value='y'):
            template.run()
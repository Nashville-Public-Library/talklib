'''
getting started with some general tests for the talklib module via Pytest.
'''
import pytest
from unittest.mock import patch

from talklib import TLShow
from .. import mock
from ..mock import RSS_URL


@pytest.fixture()
def template():
    test = TLShow()
    test.show = 'Delete Me'
    test.show_filename = 'delete_me'
    test.url = RSS_URL

    test.destinations = mock.mock_destinations()

    # disable notifications for testing. Need separate tests for these!
    test.notifications.enable_all = False
    
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
    non_updated_feed = 'https://www.pythonpodcast.com/rss' # hasn't been updated in a while.
    template.url = non_updated_feed
    with pytest.raises(Exception):
        with patch('builtins.input', return_value='y'):
            template.run()
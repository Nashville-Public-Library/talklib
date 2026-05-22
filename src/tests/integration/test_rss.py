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
    
    yield

    mock.remove_destinations()

# ---------- run ----------
        
def test_run(template):
    '''implementation test with real audio. asserts that no exceptions are raised'''
    test = TLShow(
        show = 'Delete Me',
        show_filename = 'delete_me',
        url = RSS_URL,
        destinations = mock.mock_destinations()
    )
    test.run()

def test_run2(template):
    '''assert exception raised with invalid URL'''
    test = TLShow(
        show = 'Delete Me',
        show_filename = 'delete_me',
        url = "invalid_URL",
        destinations = mock.mock_destinations()
    )
    with pytest.raises(Exception):
        test.notifications.enable_all = False
        test.run()

def test_run3(template):
    '''assert an exception is raised when the URL is a valid URL but not an rss feed'''
    test = TLShow(
        show = 'Delete Me',
        show_filename = 'delete_me',
        url = 'https://pnsne.ws/3mVuTax',
        destinations = mock.mock_destinations()
    )
    with pytest.raises(Exception):
        test.notifications.enable_all = False
        test.run()

def test_run_bad_feed(template):
    '''asserts an exception is raised for a non-updated feed'''
    test = TLShow(
        show = 'Delete Me',
        show_filename = 'delete_me',
        url = 'https://www.pythonpodcast.com/rss',
        destinations = mock.mock_destinations()
    )
    with pytest.raises(Exception):
        test.notifications.enable_all = False
        with patch('builtins.input', return_value='y'):
            test.run()
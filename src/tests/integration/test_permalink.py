import pytest

from talklib import TLShow
from .. import mock
from ..mock import env_vars, permalink


@pytest.fixture
def template():
    yield

    mock.remove_destinations()

# ---------- full run ---------- # 

def test_run(template: TLShow):
    '''asserts no exceptions are raised for the correct/normal case'''
    test = TLShow(
        show = 'Delete Me',
        show_filename = 'delete_me',
        url = permalink,
        is_permalink = True,
        destinations = mock.mock_destinations()
    )
    # disable notifications for testing. Need separate tests for these!
    test.notifications.enable_all = False
    test.run()

def test_run2(template: TLShow):
    '''asserts an exception is raised with an invalid url'''
    test = TLShow(
        show = 'Delete Me',
        show_filename = 'delete_me',
        url = "no_url",
        is_permalink = True,
        destinations = mock.mock_destinations()
    )
    with pytest.raises(Exception):
        test.run()

def test_run3(template: TLShow):
    '''assert an exception is raised with a valid URL BUT it is an RSS feed, when expecting a permalink URL'''
    test = TLShow(
        show = 'Delete Me',
        show_filename = 'delete_me',
        url = 'https://feeds.npr.org/500005/podcast.xml',
        is_permalink = True,
        destinations = mock.mock_destinations()
    )
    with pytest.raises(Exception):
        test.run()
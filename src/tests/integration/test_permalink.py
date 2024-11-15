import pytest
from unittest.mock import patch

from talklib import TLShow
from .. import mock
from ..mock import env_vars, permalink


@pytest.fixture
def template():
    with patch.dict('os.environ', env_vars):
        test = TLShow()
    test.show = 'Delete Me'
    test.show_filename = 'delete_me'
    test.url = permalink
    test.is_permalink = True

    test.destinations = mock.mock_destinations()
    # disable notifications for testing. Need separate tests for these!
    test.notifications.enable_all = False

    yield test

    mock.remove_destinations()

# ---------- full run ---------- # 

def test_run(template: TLShow):
    '''asserts no exceptions are raised for the correct/normal case'''
    template.run()

def test_run2(template: TLShow):
    '''asserts an exception is raised with an invalid url'''
    template.url = 'nourl'
    with pytest.raises(Exception):
        template.run()

def test_run3(template: TLShow):
    '''assert an exception is raised with a valid URL BUT it is an RSS feed, when expecting a permalink URL'''
    template.url = 'https://feeds.npr.org/500005/podcast.xml'
    with pytest.raises(Exception):
        template.run()
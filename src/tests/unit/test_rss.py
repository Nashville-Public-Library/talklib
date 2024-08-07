import pytest
from unittest.mock import patch

from talklib import TLShow
from ..mock import env_vars

import xml.etree.ElementTree as ET


# this RSS feed chosen as template feed because it is reliably updated every day 
# (many times per day) and because the audio file is short/small!
url = 'https://feeds.npr.org/500005/podcast.xml'


@pytest.fixture
def template_rss():
    with patch.dict('os.environ', env_vars):
        test = TLShow(
            show = 'Delete Me',
            show_filename = 'delete_me',
            url = url
        )
    # disable notifications for testing. Need separate tests for these!
    test.notifications.enable_all = False

    return test

# ---------- Misc Methods ----------

def test_check_feed_updated(template_rss: TLShow):
    assert template_rss._TLShow__check_feed_updated()

def test_get_audio_url(template_rss: TLShow):
    assert type(template_rss._TLShow__get_RSS_audio_url()) == str

def test_check_feed_loop(template_rss: TLShow):
    assert type(template_rss._TLShow__check_feed_loop()) == bool

def test_remove_yesterday_files(template_rss: TLShow):
    '''if we pass an invalid file to delete, it should be handled gracefully without exceptions'''
    template_rss._TLShow__remove(fileToDelete='not_a_file.wav')



# ---------- attribute checks ----------

def test_gen(template_rss: TLShow):
    assert type(template_rss._TLShow__create_output_filename()) == str

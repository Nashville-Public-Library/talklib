import pytest

from talklib import TLShow
from ..mock import RSS_URL


@pytest.fixture
def template_rss():
    test = TLShow()
    test.show = 'Delete Me'
    test.show_filename = 'delete_me'
    test.url = RSS_URL
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

# first, make sure there are no exceptions thrown for our correctly set up instance
def test_check_attributes_are_valid_1(template_rss: TLShow):
    template_rss._TLShow__check_attributes_are_valid()

def test_gen(template_rss: TLShow):
    assert type(template_rss._TLShow__create_output_filename()) == str

# now, start deliberately triggering exceptions with invalid attributes.

def test_check_attributes_are_valid_1a(template_rss: TLShow):
    template_rss.show = 42
    with pytest.raises(Exception):
        template_rss.__check_attributes_are_valid()

def test_check_attributes_are_valid_2(template_rss: TLShow):
    template_rss.show_filename = 42
    with pytest.raises(Exception):
        template_rss.__check_attributes_are_valid()

def test_check_attributes_are_valid_3(template_rss: TLShow):
    template_rss.url = 42
    with pytest.raises(Exception):
        template_rss.__check_attributes_are_valid()

def test_check_attributes_are_valid_6(template_rss: TLShow):
    template_rss.ffmpeg.breakaway = True
    with pytest.raises(Exception):
        template_rss.__check_attributes_are_valid()

def test_check_attributes_are_valid_7(template_rss: TLShow):
    template_rss.ffmpeg.compression_level = True
    with pytest.raises(Exception):
        template_rss.__check_attributes_are_valid()

def test_check_attributes_are_valid_8(template_rss: TLShow):
    template_rss.check_if_above = [1,2]
    with pytest.raises(Exception):
        template_rss.run()

def test_check_attributes_are_valid_9(template_rss: TLShow):
    template_rss.check_if_below = [1,2]
    with pytest.raises(Exception):
        template_rss.run()

def test_check_attributes_are_valid_10(template_rss: TLShow):
    template_rss.notifications.email_enable = 5
    with pytest.raises(Exception):
        template_rss.run()

def test_check_attributes_are_valid_11(template_rss: TLShow):
    template_rss.notifications.syslog_enable = 4.5
    with pytest.raises(Exception):
        template_rss.run()
 
def test_check_attributes_are_valid_12(template_rss: TLShow):
    '''exception should be raised if both url & is_local are declared'''
    template_rss.is_local = True
    with pytest.raises(Exception):
        template_rss.run()


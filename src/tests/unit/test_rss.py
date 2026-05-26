from pydantic_core import ValidationError
import pytest

from talklib import TLShow, FFMPEG
from talklib.notify import Notify
from ..mock import RSS_URL


@pytest.fixture
def template_rss():
    test = TLShow(
        show = 'Delete Me',
        show_filename = 'delete_me',
        url = RSS_URL
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

# first, make sure there are no exceptions thrown for our correctly set up instance
def test_check_attributes_are_valid_1(template_rss: TLShow):
    template_rss._TLShow__check_attributes_are_valid()

def test_gen(template_rss: TLShow):
    assert type(template_rss._TLShow__create_output_filename()) == str

# now, start deliberately triggering exceptions with invalid attributes.

def test_check_attributes_are_valid_6():
    with pytest.raises(ValidationError):
        ff = FFMPEG()
        ff.breakaway = True
        test = TLShow(
            show = 'Delete Me',
            show_filename = 'delete_me',
            url = RSS_URL,
            ffmpeg=ff
        )

def test_check_attributes_are_valid_7():
    with pytest.raises(ValidationError):
        ff = FFMPEG()
        ff.compression_level = True
        test = TLShow(
            show = 'Delete Me',
            show_filename = 'delete_me',
            url = RSS_URL,
            ffmpeg=ff
        )

def test_check_attributes_are_valid_8():
    with pytest.raises(ValidationError):
        test = TLShow(
            show = 'Delete Me',
            show_filename = 'delete_me',
            url = RSS_URL,
            check_if_above=[1,2]
        )

def test_check_attributes_are_valid_9():
    with pytest.raises(ValidationError):
        test = TLShow(
            show = 'Delete Me',
            show_filename = 'delete_me',
            url = RSS_URL,
            check_if_below=[1,2]
        )

def test_check_attributes_are_valid_10():
    notif = Notify()
    notif.email_enable = 5
    with pytest.raises(ValidationError):
        test = TLShow(
            show = 'Delete Me',
            show_filename = 'delete_me',
            url = RSS_URL,
            notifications=notif
        )

def test_check_attributes_are_valid_11():
    notif = Notify()
    notif.syslog_enable = 4.5
    with pytest.raises(ValidationError):
        test = TLShow(
            show = 'Delete Me',
            show_filename = 'delete_me',
            url = RSS_URL,
            notifications=notif
        )
 
def test_check_attributes_are_valid_12():
    '''exception should be raised if both url & is_local are declared'''
    with pytest.raises(ValidationError):
        test = TLShow(
            show = 'Delete Me',
            show_filename = 'delete_me',
            url = RSS_URL,
            is_local=True
        )


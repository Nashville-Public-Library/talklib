import pytest

from talklib import TLShow
import xml.etree.ElementTree as ET


# this RSS feed chosen as template feed because it is reliably updated every day 
# (many times per day) and because the audio file is short/small!
url = 'https://feeds.npr.org/500005/podcast.xml'

@pytest.fixture
def template():
    test = TLShow()
    test.show = 'Delete Me'
    test.show_filename = 'delete_me'
    test.url = url
    # disable notifications for testing. Need separate tests for these!
    test.notifications = False
    test.syslog_enable = False

    return test

# ---------- Misc Methods ----------

def test_decide_whether_to_remove(template: TLShow):
    '''
    for RSS shows, we always want to remove the source file,
    which is the file we download from the RSS feed. so this
    should always be true
    '''
    assert template.decide_whether_to_remove()

def test_get_feed(template: TLShow):
    '''check whether return object is an instance of ET.Element class'''
    assert (isinstance(template.get_feed(), ET.Element))

def test_get_feed_fails_with_invalid_url(template: TLShow):
    '''check an exception is raised when an invalid url is used'''
    template.url = 'nourl'
    with pytest.raises(Exception):
        template.run()

def test_check_feed_updated(template: TLShow):
    assert template.check_feed_updated()

def test_get_audio_url(template: TLShow):
    assert type(template.get_RSS_audio_url()) == str

def test_check_feed_loop(template: TLShow):
    assert type(template.check_feed_loop()) == bool

def test_remove_yesterday_files(template: TLShow):
    '''if we pass an invalid file to delete, it should be handled gracefully without exceptions'''
    template.remove(fileToDelete='not_a_file.wav')



# ---------- attribute checks ----------

# first, make sure there are no exceptions thrown for our correctly set up instance
def test_check_attributes_are_valid_1(template: TLShow):
    template.check_attributes_are_valid()

def test_gen(template: TLShow):
    assert type(template.create_output_filename()) == str

# now, start deliberatly triggering exceptions with invalid attributes.

def test_check_attributes_are_valid_1a(template: TLShow):
    template.show = 42
    with pytest.raises(Exception):
        template.check_attributes_are_valid()

def test_check_attributes_are_valid_2(template: TLShow):
    template.show_filename = 42
    with pytest.raises(Exception):
        template.check_attributes_are_valid()

def test_check_attributes_are_valid_3(template: TLShow):
    template.url = 42
    with pytest.raises(Exception):
        template.check_attributes_are_valid()

def test_check_attributes_are_valid_6(template: TLShow):
    template.breakaway = True
    with pytest.raises(Exception):
        template.check_attributes_are_valid()

def test_check_attributes_are_valid_7(template: TLShow):
    template.ff_level = True
    with pytest.raises(Exception):
        template.check_attributes_are_valid()

def test_check_attributes_are_valid_8(template: TLShow):
    template.check_if_above = [1,2]
    with pytest.raises(Exception):
        template.run()

def test_check_attributes_are_valid_9(template: TLShow):
    template.check_if_below = [1,2]
    with pytest.raises(Exception):
        template.run()

def test_check_attributes_are_valid_10(template: TLShow):
    template.notifications = 5
    with pytest.raises(Exception):
        template.run()

def test_check_attributes_are_valid_11(template: TLShow):
    template.twilio_enable = 4.5
    with pytest.raises(Exception):
        template.run()
 
def test_check_attributes_are_valid_12(template: TLShow):
    '''exception should be raised if both url & is_local are declared'''
    template.is_local = True
    with pytest.raises(Exception):
        template.run()


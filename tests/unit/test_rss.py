import pytest

from ...show import TLShow
import xml.etree.ElementTree as ET


# this RSS feed chosen as test feed because it is reliably updated every day 
# (many times per day) and because the audio file is short/small!
url = 'https://feeds.npr.org/500005/podcast.xml'

def generate_test_instance():
    test = TLShow()
    test.show = 'Delete Me'
    test.show_filename = 'delete_me'
    test.url = url
    # disable notifications for testing. Need separate tests for these!
    test.notifications = False
    test.syslog_enable = False
    return test

# ---------- Misc Methods ----------

def test_decide_whether_to_remove():
    '''
    for RSS shows, we always want to remove the source file,
    which is the file we download from the RSS feed. so this
    should always be true
    '''
    test = generate_test_instance()
    assert test.decide_whether_to_remove()

def test_get_feed():
    '''check whether return object is an instance of ET.Element class'''
    test = generate_test_instance()
    assert (isinstance(test.get_feed(), ET.Element))

def test_get_feed_fails_with_invalid_url():
    '''check an exception is raised when an invalid url is used'''
    test = generate_test_instance()
    test.url = 'nourl'
    with pytest.raises(Exception):
        test.run()

def test_check_feed_updated():
    test = generate_test_instance()
    assert test.check_feed_updated()

def test_get_audio_url():
    test = generate_test_instance()
    assert type(test.get_RSS_audio_url()) == str

def test_check_feed_loop():
    test = generate_test_instance()
    assert type(test.check_feed_loop()) == bool


# ---------- attribute checks ----------

# first, make sure there are no exceptions thrown for our correctly set up instance
def test_check_attributes_are_valid_1():
    test = generate_test_instance()
    test.check_attributes_are_valid()

def test_gen():
    test = generate_test_instance()
    assert type(test.create_output_filename()) == str

# now, start deliberatly triggering exceptions with invalid attributes.

def test_check_attributes_are_valid_1a():
    test = generate_test_instance()
    test.show = 42
    with pytest.raises(Exception):
        test.check_attributes_are_valid()

def test_check_attributes_are_valid_2():
    test = generate_test_instance()
    test.show_filename = 42
    with pytest.raises(Exception):
        test.check_attributes_are_valid()

def test_check_attributes_are_valid_3():
    test = generate_test_instance()
    test.url = 42
    with pytest.raises(Exception):
        test.check_attributes_are_valid()

def test_check_attributes_are_valid_6():
    test = generate_test_instance()
    test.breakaway = True
    with pytest.raises(Exception):
        test.check_attributes_are_valid()

def test_check_attributes_are_valid_7():
    test = generate_test_instance()
    test.ff_level = True
    with pytest.raises(Exception):
        test.check_attributes_are_valid()

def test_check_attributes_are_valid_8():
    test = generate_test_instance()
    test.check_if_above = [1,2]
    with pytest.raises(Exception):
        test.run()

def test_check_attributes_are_valid_9():
    test = generate_test_instance()
    test.check_if_below = [1,2]
    with pytest.raises(Exception):
        test.run()

def test_check_attributes_are_valid_10():
    test = generate_test_instance()
    test.notifications = 5
    with pytest.raises(Exception):
        test.run()

def test_check_attributes_are_valid_11():
    test = generate_test_instance()
    test.twilio_enable = 4.5
    with pytest.raises(Exception):
        test.run()
 
def test_check_attributes_are_valid_12():
    '''exception should be raised if both url & is_local are declared'''
    test = generate_test_instance()
    test.is_local = True
    with pytest.raises(Exception):
        test.run()
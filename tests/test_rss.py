'''
getting started with some general tests for the talklib module via Pytest.
'''
import pytest

from talklib.show import TLShow
import xml.etree.ElementTree as ET


# this RSS feed chosen as test feed because it is reliably updated every day 
# (many times per day) and because the audio file is short/small!
url = 'https://feeds.npr.org/500005/podcast.xml'

def generate_test_instance():
    test = TLShow() 
    test.show = 'Delete Me'
    test.show_filename = 'delete_me'
    test.url = url
    test.notifications = False
    test.syslog_enable = False
    return test

def test_gen():
    test = generate_test_instance()
    assert type(test.create_output_filename()) == str

def test_attributes(): 
    test = generate_test_instance()
    assert test.ff_level == 21
    assert type(test.ff_level) == int

    assert type(test.show) == str

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

def test_check_feed_updated():
    test = generate_test_instance()
    assert test.check_feed_updated()

def test_get_audio_url():
    test = generate_test_instance()
    assert type(test.get_audio_url()) == str

def test_check_feed_loop():
    test = generate_test_instance()
    assert type(test.check_feed_loop()) == bool


# ---------- attribute checks ----------

# first, make sure there are no exceptions thrown for our correctly set up instance
def test_check_attributes_are_valid_1():
    test = generate_test_instance()
    assert test.check_attributes_are_valid()

# now, start deliberatly triggering exceptions with different invalid attributes.
# running one test per invalid attribute.

def test_check_attributes_are_valid_1():
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

def test_check_attributes_are_valid_4():
    test = generate_test_instance()
    test.is_local = 42
    with pytest.raises(Exception):
        test.check_attributes_are_valid()

def test_check_attributes_are_valid_5():
    test = generate_test_instance()
    test.local_file = 42
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
        
def test_gen2():
    '''implementation test with real audio'''
    test = generate_test_instance()
    with pytest.raises(Exception) as something:
        assert test.run() == something
    # don't forget to delete the audio
    test.remove_yesterday = True
    test.removeYesterdayFiles()

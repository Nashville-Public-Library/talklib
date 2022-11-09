'''
getting started with some general tests for the talklib module via Pytest.
'''
import pytest

from talklib.show import TLShow

# this RSS feed chosen as test feed because it is reliably updated every day 
# (many times per day) and because it is short!
url = 'https://feeds.npr.org/500005/podcast.xml'

test = TLShow() 
test.show = 'Delete Me'
test.show_filename = 'Delete_me_please'
test.url = url
test.notifications = False
test.syslog_enable = False

def test_gen():
    assert type(test.create_output_filename()) == str

def test_attributes(): 
    assert test.ff_level == 21
    assert type(test.ff_level) == int

    assert type(test.show) == str

def test_gen2():
    with pytest.raises(Exception) as b:
        assert test.run() == b

def test_get_audio_url():
    assert type(test.get_audio_url()) == str

def test_teardown():
    '''remove the audio file after the tests have run'''
    test.remove_yesterday = True
    test.removeYesterdayFiles()

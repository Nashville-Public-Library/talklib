import atexit
import xml.etree.ElementTree as ET
import pytest
import os
import requests
import subprocess
from unittest.mock import patch

from talklib import TLShow
from ..mock import env_vars, download_test_file

permalink_URL = 'http://www.newsservice.org/LatestNC.php?ncd=MzksMzcwLDE='
RSS_URL = 'https://feeds.npr.org/500005/podcast.xml'

input_file = 'input.mp3'  # name the file we download

@pytest.fixture
def template_local():
    with patch.dict('os.environ', env_vars):
        test = TLShow()
    test.show = 'Delete Me'
    test.show_filename = 'delete_me'
    test.local_file = input_file
    test.is_local = True
    # disable notifications for testing. Need separate tests for these!
    test.notifications.syslog_enable = False
    test.notifications.twilio_enable = False
    test.notifications.email_enable = False

    yield test

@pytest.fixture
def template_permalink():
    with patch.dict('os.environ', env_vars):
        test = TLShow()
    test.show = 'Delete Me'
    test.show_filename = 'delete_me'
    test.url = permalink_URL
    test.is_permalink = True
    # disable notifications for template. Need separate templates for these!
    test.notifications.syslog_enable = False
    test.notifications.twilio_enable = False
    test.notifications.email_enable = False

    yield test

@pytest.fixture
def template_rss():
    with patch.dict('os.environ', env_vars):
        test = TLShow()
    test.show = 'Delete Me'
    test.show_filename = 'delete_me'
    test.url = RSS_URL
    # disable notifications for testing. Need separate tests for these!
    test.notifications.syslog_enable = False
    test.notifications.twilio_enable = False
    test.notifications.email_enable = False

    yield test

# ----- six digit date string -----

def test_six_digit_date_string_1(template_local: TLShow):
    '''should be of type str'''
    assert type(template_local.six_digit_date_string()) == str

def test_six_digit_date_string_2(template_local: TLShow):
    '''should always be six characters'''
    assert len(template_local.six_digit_date_string()) == 6

# ----- create output filename -----

def test_create_output_filename(template_local: TLShow):
    '''should be filename with '.wav' appended since self.include_date defaults to False'''
    assert template_local._TLShow__create_output_filename() == f'{template_local.show_filename}.wav'

def test_create_output_filename_2(template_local: TLShow):
    '''if include_date is true, datetime should be included in filename'''
    template_local.include_date = True
    assert template_local._TLShow__create_output_filename() == f'{template_local.show_filename}-{template_local.six_digit_date_string()}.wav'

def test_create_output_filename_3(template_local: TLShow):
    assert type(template_local._TLShow__create_output_filename()) == str

# ----- decide whether to remove -----

def test_decide_whether_to_remove_local_1(template_local: TLShow):
    '''should always be bool type'''
    assert type(template_local._TLShow__decide_whether_to_remove()) == bool

def test_decide_whether_to_remove_permalink_1(template_permalink: TLShow):
    '''should always be bool type'''
    assert type(template_permalink._TLShow__decide_whether_to_remove()) == bool

def test_decide_whether_to_remove_rss_1(template_rss: TLShow):
    '''should always be bool type'''
    assert type(template_rss._TLShow__decide_whether_to_remove()) == bool

def test_decide_whether_to_remove_local_2(template_local: TLShow):
    '''local files should default to not remove files'''
    assert template_local._TLShow__decide_whether_to_remove() == False

def test_decide_whether_to_remove_rss_2(template_rss: TLShow):
    '''RSS should default to True'''
    assert template_rss._TLShow__decide_whether_to_remove() == True

def test_decide_whether_to_remove_permalink_2(template_permalink: TLShow):
    '''Permalink should default to True'''
    assert template_permalink._TLShow__decide_whether_to_remove() == True

def test_decide_whether_to_remove_local_3(template_local: TLShow):
    '''should be true if we set this variable to true'''
    template_local.remove_source = True
    assert template_local._TLShow__decide_whether_to_remove()

def test_decide_whether_to_remove_permalink_3(template_permalink: TLShow):
    '''this attribute is not used for permalink shows, so should still default to True even when erroneously set to False'''
    template_permalink.remove_source = False
    assert template_permalink._TLShow__decide_whether_to_remove() == True

def test_decide_whether_to_remove_rss_3(template_rss: TLShow):
    '''permalink shows should default to True'''
    template_rss.remove_source = False
    assert template_rss._TLShow__decide_whether_to_remove() == True

# ----- convert -----
'''what else should we be testing here???'''

def test_convert_1(template_rss: TLShow):
    '''should convert and return name of file'''
    assert type(template_rss._TLShow__convert(input=download_test_file())) == str

def test_convert_2(template_local: TLShow):
    '''should convert and return name of file'''
    assert template_local._TLShow__convert(input=download_test_file()) == f'{template_local.show_filename}.wav'
    os.remove(f'{template_local.show_filename}.wav') # actually converts the file so need to remove it

def test_convert_4(template_permalink: TLShow):
    '''assert an exception is raised when ffmpeg tries to convert a non-audio file'''
    with open('test.mp3', mode='wb') as test_file:
            a = requests.get('https://library.nashville.org/themes/custom/npl/logo.svg') #not an audio file
            test_file.write(a.content)
    with pytest.raises(Exception):
        template_permalink.__convert(input=test_file.name)
    os.remove(test_file.name)

# ----- check downloaded file -----

def test_check_downloaded_file_1(template_permalink: TLShow):
    '''should raise error if file does not exist'''
    with pytest.raises(FileNotFoundError):
        template_permalink.check_downloaded_file(fileToCheck='nofile', how_many_attempts=0)

def test_check_downloaded_file_2(template_permalink: TLShow):
    '''should return True if valid file is passed'''
    assert template_permalink.check_downloaded_file(fileToCheck=download_test_file(), how_many_attempts=0) == True

def test_check_downloaded_file_3(template_permalink: TLShow):
    '''should return True if valid file is passed'''
    assert type(template_permalink.check_downloaded_file(fileToCheck=download_test_file(), how_many_attempts=0)) == bool

# ----- check length -----
'''need to test other things here...'''
def test_check_length_1(template_local: TLShow):
    
    template_local.check_if_above = 1
    template_local.check_if_below = .5
    assert type(template_local._TLShow__check_length(fileToCheck=download_test_file())) == float

# ----- get feed -----

def test_get_feed_1(template_rss: TLShow):
    '''check whether return object is an instance of ET.Element class'''
    assert (isinstance(template_rss._TLShow__get_feed(), ET.Element))

def test_get_feed_fails_with_invalid_url_1(template_rss: TLShow):
    '''check an exception is raised when an invalid url is used'''
    template_rss.url = 'nourl'
    with pytest.raises(Exception):
        template_rss.__get_feed()

# ----- check feed updated -----

def test_check_feed_updated_1(template_rss: TLShow):
    assert template_rss._TLShow__check_feed_updated()

def test_check_feed_updated_2(template_rss: TLShow):
    assert type(template_rss._TLShow__check_feed_updated()) == bool

def test_check_feed_updated_3(template_rss: TLShow):
    '''if invalid feed passed, exception should be raised'''
    template_rss.url = 'no_url'
    with pytest.raises(Exception):
        template_rss._TLShow__check_feed_updated()

# ----- check feed loop -----

def test_check_feed_loop_1(template_rss: TLShow):
    '''valid URL should return True'''
    template_rss._TLShow__check_feed_loop() == True

def test_check_feed_loop_2(template_rss: TLShow):
    '''Exception should be raised if bad URL is passed'''
    template_rss.url = 'no_url'
    with pytest.raises(Exception):
        template_rss._TLShow__check_feed_loop()

def test_check_feed_loop_3(template_rss: TLShow):
    '''should be bool type'''
    assert type(template_rss._TLShow__check_feed_loop()) == bool

# ----- old import method -----

def test_old_import_method():
    '''previous method to import the class. don't deprecate this as many scripts rely on it'''
    from talklib.show import TLShow



def teardown():
    try:
        os.remove(input_file)
    except:
        pass

atexit.register(teardown)
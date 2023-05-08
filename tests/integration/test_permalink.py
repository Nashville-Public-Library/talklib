import pytest

from ...show import TLShow

url = 'https://pnsne.ws/3mVuTax'

@pytest.fixture
def template():
    test = TLShow()
    test.show = 'Delete Me'
    test.show_filename = 'delete_me'
    test.url = url
    test.is_permalink = True
    # disable notifications for testing. Need separate tests for these!
    test.notifications = False
    test.syslog_enable = False

    return test

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

# ---------- Teardown/Cleanup ----------

def test_teardown(template: TLShow):
    '''don't forget to delete the audio'''
    template.remove_yesterday = True
    template.remove_yesterday_files()
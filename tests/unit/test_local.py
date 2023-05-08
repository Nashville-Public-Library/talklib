import pytest
import os

from ...show import TLShow

url = 'https://pnsne.ws/3mVuTax'
cwd = os.getcwd()

@pytest.fixture
def template():
    test = TLShow()
    test.show = 'Delete Me'
    test.show_filename = 'delete_me'
    test.local_file = 'some_file.mp3'
    test.is_local = True
    # disable notifications for testing. Need separate tests for these!
    test.notifications = False 
    test.syslog_enable = False

    return test

def test_decide_whether_to_remove(template: TLShow):
    '''local files should default to not remove files'''
    assert template.decide_whether_to_remove() == False

def test_decide_whether_to_remove_2(template: TLShow):
    '''should be true if we set this variable to true'''
    template.remove_source = True
    assert template.decide_whether_to_remove()

def test_check_attributes_are_valid_1(template: TLShow):
    template.is_local = None
    with pytest.raises(Exception):
        template.check_attributes_are_valid()

# ---------- check attributes ----------

def test_attrib_1a(template: TLShow):
    template.show = None
    with pytest.raises(Exception):
        template.check_attributes_are_valid()

def test_attrib_1b(template: TLShow):
    template.show = 5
    with pytest.raises(Exception):
        template.check_attributes_are_valid()

def test_attrib_1c(template: TLShow):
    template.show = True
    with pytest.raises(Exception):
        template.check_attributes_are_valid()

def test_attrib_1d(template: TLShow):
    template.show = ''
    with pytest.raises(Exception):
        template.check_attributes_are_valid()

def test_attrib_2a(template: TLShow):
    template.show_filename = None
    with pytest.raises(Exception):
        template.check_attributes_are_valid()

def test_attrib_2b(template: TLShow):
    template.show_filename = 5
    with pytest.raises(Exception):
        template.check_attributes_are_valid()

def test_attrib_2c(template: TLShow):
    template.show_filename = True
    with pytest.raises(Exception):
        template.check_attributes_are_valid()

def test_attrib_2d(template: TLShow):
    template.show_filename = ''
    with pytest.raises(Exception):
        template.check_attributes_are_valid()

def test_attrib_3a(template: TLShow):
    template.local_file = 5
    with pytest.raises(Exception):
        template.check_attributes_are_valid()

def test_attrib_3b(template: TLShow):
    template.local_file = True
    with pytest.raises(Exception):
        template.check_attributes_are_valid()

def test_attrib_4a(template: TLShow):
    template.is_local = 5
    with pytest.raises(Exception):
        template.check_attributes_are_valid()

def test_attrib_4b(template: TLShow):
    template.is_local = 'break'
    with pytest.raises(Exception):
        template.check_attributes_are_valid()
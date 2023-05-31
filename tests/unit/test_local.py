from datetime import datetime
import pytest
import os
from unittest.mock import patch, MagicMock

from ...show import TLShow
from ..mock import env_vars

url = 'https://pnsne.ws/3mVuTax'
cwd = os.getcwd()

@pytest.fixture
def template():
    with patch.dict('os.environ', env_vars):
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

def test_create_output_filename(template: TLShow):
    '''should be filename with '.wav' appended since self.include_date defaults to False'''
    assert template.create_output_filename() == f'{template.show_filename}.wav'

def test_create_output_filename_2(template: TLShow):
    '''if include_date is true, datetime should be included in filename'''
    template.include_date = True
    assert template.create_output_filename() == f'{template.show_filename}-{datetime.now().strftime("%m%d%y")}.wav'

def test_create_output_filename_3(template: TLShow):
    assert type(template.create_output_filename()) == str

# ---------- check attributes ----------

def test_check_attributes_are_valid_1(template: TLShow):
    template.is_local = None
    with pytest.raises(Exception):
        template.check_attributes_are_valid()

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
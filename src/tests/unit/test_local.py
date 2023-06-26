from datetime import datetime
import pytest
import os
from unittest.mock import patch, MagicMock

from src import TLShow
from ..mock import env_vars

url = 'https://pnsne.ws/3mVuTax'
cwd = os.getcwd()

@pytest.fixture
def template_local():
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

# ---------- check attributes ----------

def test_check_attributes_are_valid_1(template_local: TLShow):
    template_local.is_local = None
    with pytest.raises(Exception):
        template_local.check_attributes_are_valid()

def test_attrib_1a(template_local: TLShow):
    template_local.show = None
    with pytest.raises(Exception):
        template_local.check_attributes_are_valid()

def test_attrib_1b(template_local: TLShow):
    template_local.show = 5
    with pytest.raises(Exception):
        template_local.check_attributes_are_valid()

def test_attrib_1c(template_local: TLShow):
    template_local.show = True
    with pytest.raises(Exception):
        template_local.check_attributes_are_valid()

def test_attrib_1d(template_local: TLShow):
    template_local.show = ''
    with pytest.raises(Exception):
        template_local.check_attributes_are_valid()

def test_attrib_2a(template_local: TLShow):
    template_local.show_filename = None
    with pytest.raises(Exception):
        template_local.check_attributes_are_valid()

def test_attrib_2b(template_local: TLShow):
    template_local.show_filename = 5
    with pytest.raises(Exception):
        template_local.check_attributes_are_valid()

def test_attrib_2c(template_local: TLShow):
    template_local.show_filename = True
    with pytest.raises(Exception):
        template_local.check_attributes_are_valid()

def test_attrib_2d(template_local: TLShow):
    template_local.show_filename = ''
    with pytest.raises(Exception):
        template_local.check_attributes_are_valid()

def test_attrib_3a(template_local: TLShow):
    template_local.local_file = 5
    with pytest.raises(Exception):
        template_local.check_attributes_are_valid()

def test_attrib_3b(template_local: TLShow):
    template_local.local_file = True
    with pytest.raises(Exception):
        template_local.check_attributes_are_valid()

def test_attrib_4a(template_local: TLShow):
    template_local.is_local = 5
    with pytest.raises(Exception):
        template_local.check_attributes_are_valid()

def test_attrib_4b(template_local: TLShow):
    template_local.is_local = 'break'
    with pytest.raises(Exception):
        template_local.check_attributes_are_valid()
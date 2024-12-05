import pytest
import os

from talklib import TLShow
from ..mock import env_vars

url = 'http://www.newsservice.org/LatestNC.php?ncd=MzksMzcwLDE='
cwd = os.getcwd()

@pytest.fixture(autouse=True)
def mock_env_vars(monkeypatch):
    # Mock the 'destinations' environment variable globally
    for key, value in env_vars.items():
        monkeypatch.setenv(key, value)

@pytest.fixture
def template_local():
    test = TLShow()
    test.show = 'Delete Me'
    test.show_filename = 'delete_me'
    test.local_file = 'some_file.mp3'
    test.is_local = True
    # disable notifications for testing. Need separate tests for these!
    test.notifications.enable_all = False

    return test

# ---------- check attributes ----------

def test_check_attributes_are_valid_1(template_local: TLShow):
    template_local.is_local = None
    with pytest.raises(Exception):
        template_local.__check_attributes_are_valid()

def test_attrib_1a(template_local: TLShow):
    template_local.show = None
    with pytest.raises(Exception):
        template_local.__check_attributes_are_valid()

def test_attrib_1b(template_local: TLShow):
    template_local.show = 5
    with pytest.raises(Exception):
        template_local.__check_attributes_are_valid()

def test_attrib_1c(template_local: TLShow):
    template_local.show = True
    with pytest.raises(Exception):
        template_local.__check_attributes_are_valid()

def test_attrib_1d(template_local: TLShow):
    template_local.show = ''
    with pytest.raises(Exception):
        template_local.__check_attributes_are_valid()

def test_attrib_2a(template_local: TLShow):
    template_local.show_filename = None
    with pytest.raises(Exception):
        template_local.__check_attributes_are_valid()

def test_attrib_2b(template_local: TLShow):
    template_local.show_filename = 5
    with pytest.raises(Exception):
        template_local.__check_attributes_are_valid()

def test_attrib_2c(template_local: TLShow):
    template_local.show_filename = True
    with pytest.raises(Exception):
        template_local.__check_attributes_are_valid()

def test_attrib_2d(template_local: TLShow):
    template_local.show_filename = ''
    with pytest.raises(Exception):
        template_local.__check_attributes_are_valid()

def test_attrib_3a(template_local: TLShow):
    template_local.local_file = 5
    with pytest.raises(Exception):
        template_local.__check_attributes_are_valid()

def test_attrib_3b(template_local: TLShow):
    template_local.local_file = True
    with pytest.raises(Exception):
        template_local.__check_attributes_are_valid()

def test_attrib_4a(template_local: TLShow):
    template_local.is_local = 5
    with pytest.raises(Exception):
        template_local.__check_attributes_are_valid()

def test_attrib_4b(template_local: TLShow):
    template_local.is_local = 'break'
    with pytest.raises(Exception):
        template_local.__check_attributes_are_valid()
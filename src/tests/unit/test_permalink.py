import pytest
from unittest.mock import patch, MagicMock

from talklib import TLShow
from ..mock import env_vars


url = 'http://www.newsservice.org/LatestNC.php?ncd=MzksMzcwLDE='


@pytest.fixture
def template_permalink():
    with patch.dict('os.environ', env_vars):
        test = TLShow()
    test.show = 'Delete Me'
    test.show_filename = 'delete_me'
    test.url = url
    test.is_permalink = True
    # disable notifications for template. Need separate templates for these!
    test.notifications.enable_all = False

    return test

# ---------- check attributes ----------

def test_attrib_1a(template_permalink: TLShow):
    template_permalink.show = None
    with pytest.raises(Exception):
        template_permalink.__check_attributes_are_valid()

def test_attrib_1b(template_permalink: TLShow):
    template_permalink.show = 5
    with pytest.raises(Exception):
        template_permalink.__check_attributes_are_valid()

def test_attrib_1c(template_permalink: TLShow):
    template_permalink.show = True
    with pytest.raises(Exception):
        template_permalink.__check_attributes_are_valid()

def test_attrib_1d(template_permalink: TLShow):
    template_permalink.show = ''
    with pytest.raises(Exception):
        template_permalink.__check_attributes_are_valid()

def test_attrib_2a(template_permalink: TLShow):
    template_permalink.show_filename = None
    with pytest.raises(Exception):
        template_permalink.__check_attributes_are_valid()

def test_attrib_2b(template_permalink: TLShow):
    template_permalink.show_filename = 5
    with pytest.raises(Exception):
        template_permalink.__check_attributes_are_valid()

def test_attrib_2c(template_permalink: TLShow):
    template_permalink.show_filename = True
    with pytest.raises(Exception):
        template_permalink.__check_attributes_are_valid()

def test_attrib_2d(template_permalink: TLShow):
    template_permalink.show_filename = ''
    with pytest.raises(Exception):
        template_permalink.__check_attributes_are_valid()

def test_attrib_3a(template_permalink: TLShow):
    template_permalink.url = 5
    with pytest.raises(Exception):
        template_permalink.__check_attributes_are_valid()

def test_attrib_3b(template_permalink: TLShow):
    template_permalink.url = True
    with pytest.raises(Exception):
        template_permalink.__check_attributes_are_valid()

def test_attrib_4b(template_permalink: TLShow):
    template_permalink.is_permalink = 5
    with pytest.raises(Exception):
        template_permalink.__check_attributes_are_valid()

def test_attrib_4c(template_permalink: TLShow):
    template_permalink.is_permalink = 'not boolean'
    with pytest.raises(Exception):
        template_permalink.__check_attributes_are_valid()
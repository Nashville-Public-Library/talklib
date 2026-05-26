import pytest
import os

from pydantic_core import ValidationError

from talklib import TLShow
from ..mock import env_vars


url = 'http://www.newsservice.org/LatestNC.php?ncd=MzksMzcwLDE='
cwd = os.getcwd()

# ---------- check attributes ----------

def test_check_attributes_are_valid_1():
    with pytest.raises(ValidationError):
        test = TLShow(
            show = 'Delete Me',
            show_filename = 'delete_me',
            local_file = 'some_file.mp3',
            is_local = None
            )

def test_attrib_1a():
    with pytest.raises(ValidationError):
        test = TLShow(
            show = 'Delete Me',
            show_filename = 'delete_me',
            local_file = None,
            is_local = None
            )

def test_attrib_1b():
    with pytest.raises(ValidationError):
        test = TLShow(
            show = 'Delete Me',
            show_filename = 'delete_me',
            local_file = 5,
            is_local = None
            )

def test_attrib_1d():
    with pytest.raises(ValidationError):
        test = TLShow(
            show = 'Delete Me',
            show_filename = 'delete_me',
            local_file = "",
            is_local = None
            )

def test_attrib_2a():
    with pytest.raises(ValidationError):
        test = TLShow(
            show = 'Delete Me',
            show_filename = None,
            local_file = 'some_file.mp3',
            is_local = None
            )

def test_attrib_2b():
    with pytest.raises(ValidationError):
        test = TLShow(
            show = 'Delete Me',
            show_filename = 5,
            local_file = 'some_file.mp3',
            is_local = None
            )

def test_attrib_2c():
    with pytest.raises(ValidationError):
        test = TLShow(
            show = 'Delete Me',
            show_filename = True,
            local_file = 'some_file.mp3',
            is_local = None
            )

def test_attrib_2d():
    with pytest.raises(ValidationError):
        test = TLShow(
            show = 'Delete Me',
            show_filename = "",
            local_file = 'some_file.mp3',
            is_local = None
            )

def test_attrib_4b():
    with pytest.raises(ValidationError):
        test = TLShow(
            show = 'Delete Me',
            show_filename = 'delete_me',
            local_file = 'some_file.mp3',
            is_local = "hmmmm"
            )
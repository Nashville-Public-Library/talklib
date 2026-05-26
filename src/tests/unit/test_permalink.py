from pydantic_core import ValidationError
import pytest


from talklib import TLShow
from ..mock import env_vars


url = 'http://www.newsservice.org/LatestNC.php?ncd=MzksMzcwLDE='


# ---------- check attributes ----------

def test_attrib_1a():
        '''valid case, no errors/exceptions'''
        test = TLShow(
            show = 'Delete Me',
            show_filename = 'delete_me',
            url = url,
            is_permalink = True
        )

def test_attrib_1b():
    with pytest.raises(ValidationError):
        test = TLShow(
            show = 5,
            show_filename = 'delete_me',
            url = url,
            is_permalink = True
        )

def test_attrib_1c():
    with pytest.raises(ValidationError):
        test = TLShow(
            show = True,
            show_filename = 'delete_me',
            url = url,
            is_permalink = True
        )

def test_attrib_1d():
    with pytest.raises(ValidationError):
        test = TLShow(
            show = "",
            show_filename = 'delete_me',
            url = url,
            is_permalink = True
        )

def test_attrib_2a():
    with pytest.raises(ValidationError):
        test = TLShow(
            show = 'Delete Me',
            show_filename = None,
            url = url,
            is_permalink = True
        )

def test_attrib_2b():
    with pytest.raises(ValidationError):
        test = TLShow(
            show = 'Delete Me',
            show_filename = 5,
            url = url,
            is_permalink = True
        )

def test_attrib_2d():
    with pytest.raises(ValidationError):
        test = TLShow(
            show = 'Delete Me',
            show_filename = "",
            url = url,
            is_permalink = True
        )

def test_attrib_3a():
    with pytest.raises(ValidationError):
        test = TLShow(
            show = 'Delete Me',
            show_filename = 'delete_me',
            url = 5,
            is_permalink = True
        )

def test_attrib_3b():
    with pytest.raises(ValidationError):
        test = TLShow(
            show = 'Delete Me',
            show_filename = 'delete_me',
            url = True,
            is_permalink = True
        )

def test_attrib_4b():
    with pytest.raises(ValidationError):
        test = TLShow(
            show = 'Delete Me',
            show_filename = 'delete_me',
            url = url,
            is_permalink = 5
        )

def test_attrib_4c():
    with pytest.raises(ValidationError):
        test = TLShow(
            show = 'Delete Me',
            show_filename = 'delete_me',
            url = url,
            is_permalink = "Not Boolean"
        )
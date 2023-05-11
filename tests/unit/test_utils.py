import os
import pytest

try:
    from ... import utils
except KeyError:
    pass

try:
    from ...show import TLShow
except KeyError:
    pass

cwd = os.getcwd()

# talklib.utils

def test_get_timestamp():
    'should be string, not datetime object'
    assert type(utils.get_timestamp()) == str

def test_today_is_weekday():
    'should be boolean'
    assert type(utils.today_is_weekday()) == bool

def test_send_sms():
    'should raise error if argument not passed'
    with pytest.raises(TypeError):
        utils.send_sms()

def test_send_call():
    'should raise error if argument not passed'
    with pytest.raises(TypeError):
        utils.send_call()
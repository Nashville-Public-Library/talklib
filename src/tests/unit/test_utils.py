import os
import pytest
from unittest.mock import patch, MagicMock
from ..mock import env_vars
with patch.dict('os.environ', env_vars):
    from talklib.notify import Notify
    from talklib import utils

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
        Notify.send_sms()

def test_send_call():
    'should raise error if argument not passed'
    with pytest.raises(TypeError):
        Notify.send_call()
# import os
# import pytest
# from unittest.mock import patch, MagicMock

# from ... import utils

# cwd = os.getcwd()

# @pytest.fixture
# def mock_EV():
#     with patch('utils.EV') as mock:
#         instance = mock.return_value
#         instance = MagicMock(side_effect=Exception('Mocked exception'))

#         yield mock

# # talklib.utils

# def test_get_timestamp(mock_EV):
#     'should be string, not datetime object'
#     assert type(utils.get_timestamp()) == str

# def test_today_is_weekday(mock_EV):
#     'should be boolean'
#     assert type(utils.today_is_weekday()) == bool

# def test_send_sms(mock_EV):
#     'should raise error if argument not passed'
#     with pytest.raises(TypeError):
#         utils.send_sms()

# def test_send_call(mock_EV):
#     'should raise error if argument not passed'
#     with pytest.raises(TypeError):
#         utils.send_call()
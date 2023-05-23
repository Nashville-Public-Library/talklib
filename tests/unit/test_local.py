# from datetime import datetime
# import pytest
# import os

# from unittest.mock import patch, MagicMock


# from ...show import TLShow

# url = 'https://pnsne.ws/3mVuTax'
# cwd = os.getcwd()

# @pytest.fixture
# def mock_EV():
#     with patch('show.EV') as mock:
#         instance = mock.return_value
#         instance = MagicMock(side_effect=Exception('Mocked exception'))

#         yield mock

# @pytest.fixture
# def template():
#     test = TLShow()
#     test.show = 'Delete Me'
#     test.show_filename = 'delete_me'
#     test.local_file = 'some_file.mp3'
#     test.is_local = True
#     # disable notifications for testing. Need separate tests for these!
#     test.notifications = False 
#     test.syslog_enable = False

#     return test

# def test_decide_whether_to_remove(template: TLShow, mock_EV):
#     '''local files should default to not remove files'''
#     assert template.decide_whether_to_remove() == False

# def test_decide_whether_to_remove_2(template: TLShow, mock_EV):
#     '''should be true if we set this variable to true'''
#     template.remove_source = True
#     assert template.decide_whether_to_remove()

# def test_create_output_filename(template: TLShow, mock_EV):
#     '''should be filename with '.wav' appended since self.include_date defaults to False'''
#     assert template.create_output_filename() == f'{template.show_filename}.wav'

# def test_create_output_filename_2(template: TLShow, mock_EV):
#     '''if include_date is true, datetime should be included in filename'''
#     template.include_date = True
#     assert template.create_output_filename() == f'{template.show_filename}-{datetime.now().strftime("%m%d%y")}.wav'

# def test_create_output_filename_3(template: TLShow, mock_EV):
#     assert type(template.create_output_filename()) == str

# # ---------- check attributes ----------

# def test_check_attributes_are_valid_1(template: TLShow, mock_EV):
#     template.is_local = None
#     with pytest.raises(Exception):
#         template.check_attributes_are_valid()

# def test_attrib_1a(template: TLShow, mock_EV):
#     template.show = None
#     with pytest.raises(Exception):
#         template.check_attributes_are_valid()

# def test_attrib_1b(template: TLShow, mock_EV):
#     template.show = 5
#     with pytest.raises(Exception):
#         template.check_attributes_are_valid()

# def test_attrib_1c(template: TLShow, mock_EV):
#     template.show = True
#     with pytest.raises(Exception):
#         template.check_attributes_are_valid()

# def test_attrib_1d(template: TLShow, mock_EV):
#     template.show = ''
#     with pytest.raises(Exception):
#         template.check_attributes_are_valid()

# def test_attrib_2a(template: TLShow, mock_EV):
#     template.show_filename = None
#     with pytest.raises(Exception):
#         template.check_attributes_are_valid()

# def test_attrib_2b(template: TLShow, mock_EV):
#     template.show_filename = 5
#     with pytest.raises(Exception):
#         template.check_attributes_are_valid()

# def test_attrib_2c(template: TLShow, mock_EV):
#     template.show_filename = True
#     with pytest.raises(Exception):
#         template.check_attributes_are_valid()

# def test_attrib_2d(template: TLShow, mock_EV):
#     template.show_filename = ''
#     with pytest.raises(Exception):
#         template.check_attributes_are_valid()

# def test_attrib_3a(template: TLShow, mock_EV):
#     template.local_file = 5
#     with pytest.raises(Exception):
#         template.check_attributes_are_valid()

# def test_attrib_3b(template: TLShow, mock_EV):
#     template.local_file = True
#     with pytest.raises(Exception):
#         template.check_attributes_are_valid()

# def test_attrib_4a(template: TLShow, mock_EV):
#     template.is_local = 5
#     with pytest.raises(Exception):
#         template.check_attributes_are_valid()

# def test_attrib_4b(template: TLShow, mock_EV):
#     template.is_local = 'break'
#     with pytest.raises(Exception):
#         template.check_attributes_are_valid()
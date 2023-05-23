# import pytest
# from unittest.mock import patch, MagicMock

# from ...show import TLShow
# from . import mock

# url = 'https://pnsne.ws/3mVuTax'

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
#     test.url = url
#     test.is_permalink = True

#     test.destinations = mock.mock_destinations()
#     # disable notifications for testing. Need separate tests for these!
#     test.notifications = False
#     test.syslog_enable = False

#     yield test

#     mock.remove_destinations()

# # ---------- full run ---------- # 

# def test_run(template: TLShow, mock_EV):
#     '''asserts no exceptions are raised for the correct/normal case'''
#     template.run()

# def test_run2(template: TLShow, mock_EV):
#     '''asserts an exception is raised with an invalid url'''
#     template.url = 'nourl'
#     with pytest.raises(Exception):
#         template.run()

# def test_run3(template: TLShow, mock_EV):
#     '''assert an exception is raised with a valid URL BUT it is an RSS feed, when expecting a permalink URL'''
#     template.url = 'https://feeds.npr.org/500005/podcast.xml'
#     with pytest.raises(Exception):
#         template.run()
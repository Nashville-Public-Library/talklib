import pytest

from ...show import TLShow

url = 'https://pnsne.ws/3mVuTax'

def generate_test_instance():
    test = TLShow()
    test.show = 'Delete Me'
    test.show_filename = 'delete_me'
    test.url = url
    test.is_permalink = True
    # disable notifications for testing. Need separate tests for these!
    test.notifications = False
    test.syslog_enable = False
    return test

# ---------- check attributes ----------

def test_attrib_1a():
    test = generate_test_instance()
    test.show = None
    with pytest.raises(Exception):
        test.check_attributes_are_valid()

def test_attrib_1b():
    test = generate_test_instance()
    test.show = 5
    with pytest.raises(Exception):
        test.check_attributes_are_valid()

def test_attrib_1c():
    test = generate_test_instance()
    test.show = True
    with pytest.raises(Exception):
        test.check_attributes_are_valid()

def test_attrib_1d():
    test = generate_test_instance()
    test.show = ''
    with pytest.raises(Exception):
        test.check_attributes_are_valid()

def test_attrib_2a():
    test = generate_test_instance()
    test.show_filename = None
    with pytest.raises(Exception):
        test.check_attributes_are_valid()

def test_attrib_2b():
    test = generate_test_instance()
    test.show_filename = 5
    with pytest.raises(Exception):
        test.check_attributes_are_valid()

def test_attrib_2c():
    test = generate_test_instance()
    test.show_filename = True
    with pytest.raises(Exception):
        test.check_attributes_are_valid()

def test_attrib_2d():
    test = generate_test_instance()
    test.show_filename = ''
    with pytest.raises(Exception):
        test.check_attributes_are_valid()

def test_attrib_3a():
    test = generate_test_instance()
    test.url = 5
    with pytest.raises(Exception):
        test.check_attributes_are_valid()

def test_attrib_3b():
    test = generate_test_instance()
    test.url = True
    with pytest.raises(Exception):
        test.check_attributes_are_valid()

def test_attrib_4b():
    test = generate_test_instance()
    test.is_permalink = 5
    with pytest.raises(Exception):
        test.check_attributes_are_valid()

def test_attrib_4c():
    test = generate_test_instance()
    test.is_permalink = 'not boolean'
    with pytest.raises(Exception):
        test.check_attributes_are_valid()

# ---------- full run ---------- # 

def test_run():
    '''asserts no exceptions are raised for the correct/normal case'''
    test = generate_test_instance()
    test.run()

def test_run2():
    '''asserts an exception is raised with an invalid url'''
    test = generate_test_instance()
    test.url = 'nourl'
    with pytest.raises(Exception):
        test.run()

# ---------- Teardown/Cleanup ----------

def test_teardown():
    '''don't forget to delete the audio'''
    test = generate_test_instance()
    test.remove_yesterday = True
    test.removeYesterdayFiles()

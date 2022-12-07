import pytest
import os

from ...show import TLShow

url = 'https://pnsne.ws/3mVuTax'
cwd = os.getcwd()

def generate_test_instance():
    test = TLShow()
    test.show = 'Delete Me'
    test.show_filename = 'delete_me'
    
    # this is ugly. i am sorry
    if 'tests\\' in cwd:
        test.local_file = 'local_test_file.mp3'
    else: 
        test.local_file = 'tests\\local_test_file.mp3'

    test.is_local = True
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
    test.local_file = 5
    with pytest.raises(Exception):
        test.check_attributes_are_valid()

def test_attrib_3b():
    test = generate_test_instance()
    test.local_file = True
    with pytest.raises(Exception):
        test.check_attributes_are_valid()

def test_attrib_4a():
    test = generate_test_instance()
    test.is_local = 5
    with pytest.raises(Exception):
        test.check_attributes_are_valid()

def test_attrib_4b():
    test = generate_test_instance()
    test.is_local = 'break'
    with pytest.raises(Exception):
        test.check_attributes_are_valid()
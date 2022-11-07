'''
getting started with some general tests for the talklib module via Pytest.
'''
import pytest

from talklib.show import TLShow

a = TLShow() 
a.show = 'some show'
a.show_filename = 'some_show'
a.url = 'some_site'

def test_gen():
    assert type(a.create_output_filename()) == str

def test_gen1():             
    assert a.ff_level == 21

def test_gen2():
    a.notifications = False
    with pytest.raises(expected_exception=Exception) as b:
        assert a.run() == b

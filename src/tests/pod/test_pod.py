from unittest.mock import patch

from pydantic_core import ValidationError
import pytest

from .mock import env_vars
with patch.dict('os.environ', env_vars):
    from talklib import TLPod
    from talklib.pod import AWS


def test_type_1():
    '''pydantic should raise an error if wrong type passed in'''
    with pytest.raises(ValidationError):
            test = TLPod(
                show=5, 
                show_filename="del",
                bucket_folder='nope')
            
def test_type_2():
    '''pydantic should raise an error if wrong type passed in'''
    with pytest.raises(ValidationError):
            test = TLPod(
                show=5, 
                show_filename=5,
                bucket_folder='nope')

def test_type_3():
    '''pydantic should raise an error if wrong type passed in'''
    with pytest.raises(ValidationError):
            test = TLPod(
                show='delete', 
                show_filename="del",
                bucket_folder=5)
            
def test_buckets():
    a = AWS()
    a.print_buckets()
    a.print_folders()
    a.print_files()
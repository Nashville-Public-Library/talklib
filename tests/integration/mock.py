import os
import shutil

def mock_destinations():
    destinations = ['dest1', 'dest2', 'dest3']
    for destination in destinations:
        if not os.path.exists(destination):
            os.mkdir(destination)
    return destinations

def remove_destinations():
    for destination in mock_destinations():
        shutil.rmtree(destination)
import os
import requests
import shutil


'''
We need to test 'local' files - meaning files we already have downloaded. But we don't want
to have to put an audio file into Git. So we're using this static URL to download first,
to mock a local file. Downloading the file itself it just setting up the test.

This static link was chosen because it's reliably available and the file is small/short.
'''
permalink = "http://www.newsservice.org/LatestNC.php?ncd=MzksMzcwLDI="
RSS_URL = "https://feeds.megaphone.fm/ESP9792844572"

env_vars = {
        'destinations': 'nothing',
        'syslog_server': 'mocked_value2',
        'fromEmail': 'mocked_value2',
        'toEmail': 'mocked_value2',
        'mail_server_external': 'mocked_value2',
        'twilio_sid': 'mocked_value2',
        'twilio_token': 'mocked_value2',
        'twilio_from': 'mocked_value2',
        'twilio_to': 'mocked_value2',
        'icecast_user': 'mahhhh',
        'icecast_pass': 'mahhhhh'
    }

def mock_destinations():
    destinations = ['dest1', 'dest2', 'dest3']
    for destination in destinations:
        if not os.path.exists(destination):
            os.mkdir(destination)
    return destinations

def remove_destinations():
    for destination in mock_destinations():
        shutil.rmtree(destination)
    
def download_test_file():
    input_file = 'input.mp3'  # name the file we download
    downloaded_file = input_file
    file_exists = os.path.isfile(input_file)
    if not file_exists:
        with open (input_file, mode='wb') as downloaded_file:
            a = requests.get(permalink)
            downloaded_file.write(a.content)
            downloaded_file.close()
            return downloaded_file.name
    return downloaded_file
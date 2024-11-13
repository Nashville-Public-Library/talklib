import os
import requests


'''
We need to test 'local' files - meaning files we already have downloaded. But we don't want
to have to put an audio file into Git. So we're using this static URL to download first,
to mock a local file. Downloading the file itself it just setting up the test.

This static link was chosen because it's reliably available and the file is small/short.
'''
permalink = "http://www.newsservice.org/LatestNC.php?ncd=MzksMzcwLDI="
RSS_URL = "https://feeds.megaphone.fm/ESP9792844572"

def mock_destinations():
    destination = 'dest1'
    if not os.path.exists(destination):
            os.mkdir(destination)
    return destination

env_vars = {
        'destinations': mock_destinations(),
        'syslog_server': '10.10.10.10',
        'fromEmail': 'mocked_value2',
        'toEmail': 'mocked_value2',
        'mail_server_external': 'mocked_value2',
        'twilio_sid': 'mocked_value2',
        'twilio_token': 'mocked_value2',
        'twilio_from': 'mocked_value2',
        'twilio_to': 'mocked_value2',
        'icecast_user': 'mahhhh',
        'icecast_pass': 'mahhhhh',
        'pod_server_uname': 'mahhhhh'
    }

    
def download_test_file(filename: str = 'input.mp3'):
    downloaded_file = filename
    file_exists = os.path.isfile(filename)
    if not file_exists:
        with open (filename, mode='wb') as downloaded_file:
            a = requests.get(permalink)
            downloaded_file.write(a.content)
            downloaded_file.close()
            return downloaded_file.name

    return downloaded_file
import os
import shutil

permalink = 'https://pnsne.ws/3mVuTax'

env_vars = {
        'OnAirPC': 'nothing',
        'ProductionPC': 'mocked_value2',
        'syslog_server': 'mocked_value2',
        'fromEmail': 'mocked_value2',
        'toEmail': 'mocked_value2',
        'mail_server_external': 'mocked_value2',
        'twilio_sid': 'mocked_value2',
        'twilio_token': 'mocked_value2',
        'twilio_from': 'mocked_value2',
        'twilio_to': 'mocked_value2',
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
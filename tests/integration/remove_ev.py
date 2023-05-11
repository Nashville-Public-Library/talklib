from pytest import MonkeyPatch

def remove_EV():
    return MonkeyPatch().setenv(name='OnAirPC', value='mah'), 
MonkeyPatch().setenv(name='ProductionPC', value='mah'),
MonkeyPatch().setenv(name='syslog_server', value='mah'),
MonkeyPatch().setenv(name='fromEmail', value='mah'),
MonkeyPatch().setenv(name='toEmail', value='mah'),
MonkeyPatch().setenv(name='mail_server_external', value='mah'),
MonkeyPatch().setenv(name='twilio_sid', value='mah'),
MonkeyPatch().setenv(name='twilio_token', value='mah'),
MonkeyPatch().setenv(name='twilio_from', value='mah'),
MonkeyPatch().setenv(name='twilio_to', value='mah'),
MonkeyPatch().setenv(name='OnAirPC', value='mah'),
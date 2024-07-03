from email.message import EmailMessage
from enum import Enum
import logging
from logging.handlers import SysLogHandler
import smtplib

from twilio.rest import Client

from talklib.ev import EV

class LogLevel(Enum):
    INFO = logging.INFO
    DEBUG = logging.DEBUG
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL

class Syslog:
    def __init__ (self):
        self.syslog_host = EV().syslog_host
        self.syslog_port = 514

    def send_syslog_message(self, message: str, level: str = 'info'):
        '''
        Send message to Syslog server.
        Levels: info (default), debug, warning, error, critical.

        The level type and the my_logger.method() function must match!
        '''
        handler = SysLogHandler(address=(self.syslog_host, self.syslog_port))

        my_logger = logging.getLogger('MyLogger')
        my_logger.setLevel(LogLevel[level.upper()].value)
        my_logger.addHandler(handler)

        my_logger.log(level=LogLevel[level.upper()].value, msg=message)
        my_logger.removeHandler(handler) # don't forget this after you send the message!

class Notify:
    def __init__ (self,
                  enable_all: bool = True,
                  syslog_enable: bool = True,
                  twilio_enable: bool = True,
                  email_enable: bool = True,
                  ):
        
        self.enable_all = enable_all
        self.syslog_enable = syslog_enable
        self.twilio_enable = twilio_enable
        self.email_enable = email_enable
        self.syslog = Syslog()
        self.EV = EV()

    def send_syslog(self, message: str, level: str) -> None:
        '''send message to syslog server'''
        if not (self.syslog_enable and self.enable_all):
            return
        self.syslog.send_syslog_message(message=message, level=level)
    
    def send_call(self, message: str) -> None:
        '''send voice call via twilio'''
        if not (self.twilio_enable and self.enable_all):
            return
        for number in self.EV.twilio_to:
            client = Client(self.EV.twilio_sid, self.EV.twilio_token)

            call = client.calls.create(
                                    twiml=f'<Response><Say>{message}</Say></Response>',
                                    to=number,
                                    from_=self.EV.twilio_from
                                )
            call.sid

    def send_sms(self, message: str) -> None:
        '''send sms via twilio. '''
        if not (self.twilio_enable and self.enable_all):
            return
        for number in self.EV.twilio_to:
            client = Client(self.EV.twilio_sid, self.EV.twilio_token)
            SMS = client.messages.create(
                body=message,
                from_=self.EV.twilio_from,
                to=number
            )
            SMS.sid

    def send_mail(self, message: str, subject: str) -> None:
        '''send email to TL gmail account via relay address'''
        if not (self.email_enable and self.enable_all):
            return
        for email in self.EV.toEmail:
            format = EmailMessage()
            format.set_content(message)
            format['Subject'] = subject
            format['From'] = self.EV.fromEmail
            format['To'] = email

            mail = smtplib.SMTP(host=self.EV.mail_server)
            mail.send_message(format)
            mail.quit()
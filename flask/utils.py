from Google import Create_Service
import os
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import mimetypes
import time # for time tracker

def timethis(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print('[*] Execution time: {} seconds.'.format(end-start))
        return result
    return wrapper

class sendGmail():
    def __init__(self, sender, to, subject, text, file):
        self.to=to
        self.sender=sender
        self.subject=subject
        self.secret = "client.json"
        self.api = "gmail"
        self.version = "v1"
        self.text = text
        self.file = file

        self.service = Create_Service(self.secret, self.api, self.version)

    #create a message with attachment
    def create_message_with_attachment(self):
        message = MIMEMultipart()
        message['to'] = self.to
        message['from'] = self.sender
        message['subject'] = self.subject

        msg = MIMEText(self.text)
        message.attach(msg)

        content_type, encoding = mimetypes.guess_type(self.file)

        if content_type is None or encoding is not None:
            content_type = 'application/octet-stream'
        main_type, sub_type = content_type.split('/', 1)
        if main_type == 'text':
            fp = open(self.file, 'rb')
            msg = MIMEText(fp.read(), _subtype=sub_type)
            fp.close()
        elif main_type == 'image':
            fp = open(self.file, 'rb')
            msg = MIMEImage(fp.read(), _subtype=sub_type)
            fp.close()
        elif main_type == 'audio':
            fp = open(self.file, 'rb')
            msg = MIMEAudio(fp.read(), _subtype=sub_type)
            fp.close()
        else:
            fp = open(self.file, 'rb')
            msg = MIMEBase(main_type, sub_type)
            msg.set_payload(fp.read())
            fp.close()

        filename = os.path.basename(file)
        msg.add_header('Content-Disposition', 'attachment', filename=filename)
        message.attach(msg)

        return {'raw': base64.urlsafe_b64encode(message.as_string())}


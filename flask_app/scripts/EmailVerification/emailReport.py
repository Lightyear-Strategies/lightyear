import base64, os, mimetypes
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from flask_app.scripts.googleAuth import serviceBuilder, localServiceBuilder


class report():
    def __init__(self, sender, to, subject, text, file, user_id=None):
        self.sender = sender
        self.to = to
        self.subject = subject
        self.text = text
        self.file = file
        if user_id is None:
            self.user_id = 'me'
        else:
            self.user_id = user_id
        self.scopes = ['https://mail.google.com/']
        self.service = serviceBuilder()
        # self.service = localServiceBuilder()
        self.body = self.createMessage()
        print('Our self', self.file)


    def sendMessage(self):
        try:
            try:
                print(self.service.users())
            except Exception as e:
                print('An error occurred #1: {}'.format(e))
            message = self.service.users().messages().send(userId=self.user_id,
                                                           body=self.body).execute()

            print('Message Id: {}'.format(message['id']))
            return message
        except Exception as e:
            print('An error occurred #2: {}'.format(e))
            return None

    def createMessage(self):
        message = MIMEMultipart()
        message['to'] = self.to
        message['from'] = self.sender
        message['subject'] = self.subject

        msg = MIMEText(self.text)
        message.attach(msg)

        (contentType, encoding) = mimetypes.guess_type(self.file)

        if contentType is None or encoding is not None:
            contentType = 'application/octet-stream'

        (main_type, sub_type) = contentType.split('/', 1)

        if main_type == 'text':
            with open(self.file, 'rb') as f:
                msg = MIMEText(f.read().decode('utf-8'), _subtype=sub_type)

        elif main_type == 'image':
            with open(self.file, 'rb') as f:
                msg = MIMEImage(f.read(), _subtype=sub_type)

        elif main_type == 'audio':
            with open(self.file, 'rb') as f:
                msg = MIMEAudio(f.read(), _subtype=sub_type)

        else:
            with open(self.file, 'rb') as f:
                msg = MIMEBase(main_type, sub_type)
                msg.set_payload(f.read())

        filename = os.path.basename(self.file)
        msg.add_header('Content-Disposition', 'attachment',
                       filename=filename)
        message.attach(msg)

        raw_message = base64.urlsafe_b64encode(message.as_string().encode('utf-8'))
        return {'raw': raw_message.decode('utf-8')}


if __name__ == "__main__":
    gmail = report("aleksei@lightyearstrategies.com", "aleksei@lightyearstrategies.com",
                   "this is the subject line", "This is the message body", "./test.csv",
                   "me")
    gmail.sendMessage()

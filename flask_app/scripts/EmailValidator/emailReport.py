import base64, os, mimetypes
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.message import EmailMessage
from email.utils import make_msgid
from email.mime.application import MIMEApplication
import email.encoders
import traceback
from flask_app.scripts.googleAuth import serviceBuilder, localServiceBuilder, serviceAccountBuilder


class report():
    def __init__(self, sender, to, subject, text, file=None, user_id=None, rules=None, new_filename=None):
        self.sender = sender
        self.to = to
        print(self.to)
        self.subject = subject
        self.text = text
        self.file = file
        self.new_filename = new_filename
        self.rules = rules
        if user_id is None:
            self.user_id = 'me'
        else:
            self.user_id = user_id
        self.scopes = ['https://mail.google.com/']
        #self.service = serviceBuilder()
        #self.service = localServiceBuilder()
        if self.rules:
            self.replacePlaceholders()
        self.service = serviceAccountBuilder()
        self.body = self.createMessage()

    def sendMessage(self):
        try:
            try:
                print(self.service.users())
            except Exception as e:
                print('An error occurred #1: {}'.format(e))
            message = self.service.users().messages().send(userId=self.user_id,  body=self.body).execute()

            print('Message Id: {}'.format(message['id']))
            return message
        except Exception as e:
            traceback.print_exc()
            print('An error occurred #2: {}'.format(e))
            return None

   #Going through the dictionary of rules and replacing placeholders within HTML
   #with the arbitrary values
    def replacePlaceholders(self):
        text = self.text
        rules = self.rules
        for key, value in rules.items():
            text = text.replace(key, value)
        self.text = text


    def createMessage(self):
        message = MIMEMultipart()
        if isinstance(self.to,str):
            message['to'] = self.to
        else:
            message['to'] = ', '.join(self.to)
        #print(message['to'])
        message['from'] = self.sender
        message['subject'] = self.subject

        msg = MIMEText(self.text, 'html')
        message.attach(msg)

        if self.file:

            (content_type, encoding) = mimetypes.guess_type(self.file)

            if content_type is None or encoding is not None:
                content_type = 'application/octet-stream'

            (main_type, sub_type) = content_type.split('/', 1)

            if main_type == 'text':
                with open(self.file, 'rb') as f:
                    msg = MIMEText(f.read().decode('utf-8'), _subtype="html")

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

            if self.new_filename:
                filename = self.new_filename
            else:
                filename = os.path.basename(self.file)

            msg.add_header('Content-Disposition', 'attachment',
                           filename=filename)
            email.encoders.encode_base64(msg)
            message.attach(msg)

        raw_message = base64.urlsafe_b64encode(message.as_string().encode('utf-8'))
        return {'raw': raw_message.decode('utf-8')}

if __name__ == "__main__":
    #from flask_app.scripts.config import Config
    #gmail = report(Config.SENDER_EMAIL_NAME, "chris@lightyearstrategies.com",
    #               "this is the subject line", "This is the message body", "limit_analysis.csv",
    #               "me")
    #open .html file in assets folder
    # with open('assets/welcome.html', 'r') as f:
    #     html = f.read()
    # with open('assets/tracker.html', 'r') as f:
    #     html = f.read()

    with open("assets/topic_report.html", 'r') as f:
        html = f.read()

    # TRACKER PLACEHOLDERS
    # rules = {
    #     '{username}': 'Codrin',
    #     '{chosen_frequency}': 'week',
    #     'URL_TO_UNSUBSCRIBE': 'https://www.google.com'
    # }

    #WELCOME PLACEHOLDERS
    # rules = {
    #     '{username}': 'Codrin'
    # }

    #TOPIC SUB PLACEHOLDERS
    # rules = {
    #     '{username}': 'Codrin',
    #     '{topic}': 'AI',
    #     '{chosen_frequency}': 'week',
    #     'URL_TO_UNSUBSCRIBE': 'https://www.google.com'
    # }

    #TRACKER REPORT PLACEHOLDERS
    # rules = {
    #     '{username}': 'Codrin',
    #     "{chosen_frequency}": "weekly",
    #     'URL_TO_UNSUBSCRIBE': 'https://www.google.com',
    # }

    #TOPIC REPORT PLACEHOLDERS
    rules = {
        '{username}': 'Codrin',
        "{chosen_frequency}": "weekly",
        "{topic}": "AI",
        'URL_TO_UNSUBSCRIBE': 'https://www.google.com',
    }


    gmail = report('"George Lightyear" <george@lightyearstrategies.com>', "codrin@lightyearstrategies.com",
                   "this is the subject line", html,
                   user_id="me", rules=rules)
    gmail.sendMessage()

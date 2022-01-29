import base64
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
import mimetypes
import pickle
import os
from apiclient import errors
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import Flow  # for web
# from google_auth_oauthlib.flow import InstalledAppFlow — used for local development
from google.auth.transport.requests import Request
import json
from flaskMain import app


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
        self.service = self.__auth()
        self.body = self.createMessage()

    def __auth(self):
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = Flow.from_client_secrets_file(
                    'client.json',
                    self.scopes
                )

                with open("client.json") as jsonFile:
                    jsonObject = json.load(jsonFile)
                    jsonFile.close()
                flow.redirect_uri = jsonObject['web']['redirect_uris'][0]

                authorization_url, state = flow.authorization_url(
                    access_type='offline',
                    include_granted_scopes='true')

                #print('Please go to this URL: {}'.format(authorization_url))

                # The user will get an authorization code. This code is used to get the
                # access token.
                #code = input('Enter the authorization code: ')

                code = app.redirect(authorization_url)
                flow.fetch_token(code=code)

                #print(flow.credentials)
                creds = flow.credentials

                # return HttpResponseRedirect(authorization_url)
                """
                * for Installed App * 

                flow = InstalledAppFlow.from_client_secrets_file(
                    'client.json', self.scopes)
                creds = flow.run_local_server(port=0)
                """
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('gmail', 'v1', credentials=creds)

        return service

    def sendMessage(self):
        try:
            message = self.service.users().messages().send(userId=self.user_id,
                                                           body=self.body).execute()

            print('Message Id: {}'.format(message['id']))
            return message
        except Exception as e:
            print('An error occurred: {}'.format(e))
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

        raw_message = \
            base64.urlsafe_b64encode(message.as_string().encode('utf-8'))
        return {'raw': raw_message.decode('utf-8')}


if __name__ == "__main__":
    gmail = report("aleksei@lightyearstrategies.com", "aleksei@lightyearstrategies.com",
                   "this is the subject line", "This is the message body", "./test.csv",
                   "me")
    gmail.sendMessage()

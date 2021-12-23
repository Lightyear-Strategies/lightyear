"""A module for setting up a listener on an email. Listens for HARO emails, returns the body of any HARO emails received"""

from __future__ import print_function

import os.path 

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def print_label():
    creds = None
    # YOU WILL NEED TO GENERATE YOUR OWN OAUTH CLIENT CREDENTIALS
    # REPLACE WITH PATH TO YOUR CREDENTIALS
    if os.path.exists('/Users/liammurphy/Downloads/creds_secret/token.json'):
        creds = Credentials.from_authorized_user_file('/Users/liammurphy/Downloads/creds_secret/token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '/Users/liammurphy/Downloads/creds_secret/credentials.json', SCOPES)
            # WILL NEED TO UPDATE FOR FLASK DEPLOYMENT
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('/Users/liammurphy/Downloads/creds_secret/token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # check for new mail
        # read subject lines
        # if HARO in subject line
        # return email body as either string or dataframe
        pass

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')


if __name__ == '__main__':
    print_label()
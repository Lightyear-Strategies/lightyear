"""A module for setting up a listener on an email. Listens for HARO emails, returns the body of any HARO emails received"""

from __future__ import print_function

import time
import os.path 

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# @params = none
# @return credentials: a set of google api credentials
def authorize():
    """takes user through credentials and OAuth process, returns a set of credentials for later api use"""
    creds = None
    if os.path.exists('config/token.json'):
        creds = Credentials.from_authorized_user_file('config/token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'config/credentials.json', SCOPES)
            # WILL NEED TO UPDATE FOR FLASK DEPLOYMENT
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('config/token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

# @params email: a string of the users email, debug: do you want to debug ??
def find_haro(email : str, debug : bool = False):
    """searches through all messages in the email (all inboxes, including trash and spam) and returns the entire google api message object of the most recent HARO query email"""
    creds = authorize()
    try:
        service = build("gmail", "v1", credentials=creds)
        messages = service.users().messages()
        request = messages.list(userId=email, includeSpamTrash=True, maxResults=500)
        # dictionary ordered, good news. index 0 is most recent messages, will help optimize code
        messages_dict = request.execute()["messages"]
        if debug:
            print(messages_dict)

        if debug:
            request = messages.get(userId=email, id=messages_dict[24]['id'], format="full")
            headers = request.execute()['payload']['headers']
            to_print = None
            for dic in headers:
                if dic['name'] == "Subject":
                    to_print = dic['value']
            print(to_print)

        for mes in messages_dict:
            # to not overrun rate limit of 50 calls per second
            time.sleep(1 / 40)
            request = messages.get(userId=email, id=mes['id'], format='full')
            headers = request.execute()['payload']['headers']
            for dic in headers:
                if dic['name'] == "Subject":
                    if "[HARO]" in dic['value']:
                        # returns full message json of HARO email
                        return request.execute()
        service.close()

    except HttpError as error:
        # TO ADD: Handle errors from gmail API.
        print(f'An error occurred: {error}')


if __name__ == '__main__':
    # can write to output file, or use with Chris's parser
    find_haro("liam@lightyearstrategies.com", False)
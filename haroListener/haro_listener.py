"""A module for setting up a listener on an email. Listens for HARO emails, returns the body of any HARO emails received"""

from __future__ import print_function

import datetime
import time
import os.path 

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class HaroListener():
    """A class to wrap our haro listening function"""

    # constructor for haro listener
    # @params: email, debug
    # @return: None
    def __init__(self, email : str, debug : bool = False):
        self.email = email
        self.debug = debug
        self.scopes = ['https://www.googleapis.com/auth/gmail.readonly']

    # @params = none
    # @return credentials: a set of google api credentials
    def authorize(self):
        """takes user through credentials and OAuth process, returns a set of credentials for later api use"""
        creds = None
        if os.path.exists('config/token.json'):
            creds = Credentials.from_authorized_user_file('config/token.json', self.scopes)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'config/credentials.json', self.scopes)
                # WILL NEED TO UPDATE FOR FLASK DEPLOYMENT
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('config/token.json', 'w') as token:
                token.write(creds.to_json())
        return creds

    # @params None
    # @return json-like dict object representing the most recent HARO email
    def find_recent_haro(self):
        """searches through all messages in the email (all inboxes, including trash and spam) and returns the entire google api message object of the most recent HARO query email"""
        creds = self.authorize()
        try:
            service = build("gmail", "v1", credentials=creds)
            messages = service.users().messages()
            request = messages.list(userId=self.email, includeSpamTrash=True, maxResults=500)
            # dictionary ordered, good news. index 0 is most recent messages, will help optimize code
            messages_dict = request.execute()["messages"]
            if self.debug:
                print(messages_dict)

            if self.debug:
                request = messages.get(userId=self.email, id=messages_dict[24]['id'], format="full")
                headers = request.execute()['payload']['headers']
                to_print = None
                for dic in headers:
                    if dic['name'] == "Subject":
                        to_print = dic['value']
                print(to_print)

            for mes in messages_dict:
                # to not overrun rate limit of 50 calls per second
                time.sleep(1 / 40)
                request = messages.get(userId=self.email, id=mes['id'], format='full')
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

    # @params: None
    # @return: a json-like dict object of the new HARO email
    def listen(self):
        """Listens to email: checks one minute after HARO emails are scheduled to be release using the find_recent_haro function to return the newest HARO email"""
        est_tz = datetime.timezone(datetime.timedelta(hours = -5), "EST")

        morning_haro = datetime.time(hour=5, minute=40, second=0, tzinfo=est_tz)
        afternoon_haro = datetime.time(hour=12, minute=40, second=0, tzinfo=est_tz)
        night_haro = datetime.time(hour=17, minute=40, second=0, tzinfo=est_tz)

        while True:
            time_now = datetime.datetime.now(est_tz)
            morn = datetime.datetime.combine(time_now.date(), morning_haro)
            aft = datetime.datetime.combine(time_now.date(), afternoon_haro)
            night = datetime.datetime.combine(time_now.date(), night_haro)
            # update datetimes if needed
            if time_now > morn and time_now > aft and time_now > night:
                morn = morn + datetime.timedelta(days=1)
                aft = aft + datetime.timedelta(days=1)
                night = night + datetime.timedelta(days=1)
            # find next haro
            next_haro = min({td for td in {morn - time_now, aft - time_now, night - time_now} if td > datetime.timedelta(0)})
            time.sleep(next_haro.total_seconds())
            # need to find a way to port this somewhere, maybe dump to json
            self.find_recent_haro()
            # to ensure time_now updates correctly
            time.sleep(60)



if __name__ == '__main__':
    # can write to output file, or use with Chris's parser
    HaroListener("liam@lightyearstrategies.com", False).listen()
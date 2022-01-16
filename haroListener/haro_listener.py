"""A module for setting up a listener on an email. Listens for HARO emails, returns the body of any HARO emails received"""

from __future__ import print_function

import datetime
import base64
import json
import time
import os.path
import pickle
import pandas as pd

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from haro_parser import Haro

class HaroListener():
    """A class to wrap our haro listening function"""

    # constructor for haro listener
    # @params: email, debug
    # @return: None
    def __init__(self, email : str, debug : bool = False):
        self.email = email
        self.debug = debug
        self.scopes = ['https://mail.google.com/']
        self.creds = self.__auth()
        self.save_dir = 'haro_jsons/'

    # @params = none
    # @return credentials: a set of google api credentials
    def __auth(self):
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'client.json', self.scopes)
                creds = flow.run_local_server(port=0)
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('gmail', 'v1', credentials=creds)

        return service

    # @params None
    # @return json-like dict object representing the most recent HARO email
    def __find_recent_haro(self):
        """a helper method to sort through all messages in the email (all inboxes, including trash and spam) and returns the entire google api message object of the most recent HARO query email"""
        try:
            service = self.creds
            messages = service.users().messages()
            request = messages.list(userId=self.email, includeSpamTrash=True, maxResults=500, q='subject:[HARO]')
            # dictionary ordered, good news. index 0 is most recent messages, will help optimize code
            messages_list = request.execute()['messages']
            if self.debug:
                print(messages_list)

            if self.debug:
                request = messages.get(userId=self.email, id=messages_list[24]['id'], format='full')
                headers = request.execute()['payload']['headers']
                to_print = None
                for dic in headers:
                    if dic['name'] == "Subject":
                        to_print = dic['value']
                print(to_print)

            found = False # flag to check for messages found
            for mes in messages_list:
                # to not overrun rate limit of 50 calls per second
                time.sleep(1 / 40)
                request = messages.get(userId=self.email, id=mes['id'], format='full')
                message = request.execute()
                headers = message['payload']['headers']
                for dic in headers:
                    if dic['name'] == "Subject":
                        if "[HARO]" in dic['value']:
                            # returns full message json of HARO email
                            found = True
                            service.close()
                            haro_obj = Haro([message])
                            return haro_obj
            if not found:
                service.close()
                print("NO HARO FOUND")
                return None

        except HttpError as error:
            # TODO Handle errors from gmail API.
            print(f"An error occurred: {error}")
            print("NO HARO FOUND")

    # @params: None
    # @return: None
    def listen(self):
        """Listens to email: checks one minute after HARO emails are scheduled to be release using the __find_recent_haro method to output the newest HARO message object to json"""
        est_tz = datetime.timezone(datetime.timedelta(hours = -5), 'EST')

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
            # TODO need to find a way to port this somewhere, maybe dump to json
            self.haros_to_json([self.__find_recent_haro()])
            # to ensure time_now updates correctly
            time.sleep(60)

    # @params: from_date: a string in "yyyy-mm-dd" format
    # @return: a list of json-like dict objects representing HARO emails from `from_date` to current date.
    def find_haro_from(self, from_date : str = None):
        """finds and returns a list of message objects for every HARO email from from_date til now. returns only most recent HARO when from_date = None

        input
        from_date: string date in format yyyy-mm-dd"""
        # return most recent HARO on no input
        if from_date == None:
            return [self.__find_recent_haro()]
        # from_date MUST be in correct ISO format
        from_datetime = datetime.date.fromisoformat(from_date)
        try: 
            service = self.creds
            messages = service.users().messages()
            request = messages.list(userId=self.email, includeSpamTrash=True, maxResults=500, q='subject:[HARO]')
            page = request.execute()
            messages_list = page['messages']

            if len(messages_list) == 0:
                print("NO HARO FOUND")
                service.close()
                return None

            while "nextPageToken" in page.keys():
                # check for final date
                time.sleep(1 / 40)
                request = messages.get(userId=self.email, id=messages_list[-1]['id'], format='full')
                last_message = request.execute()
                last_date = datetime.date.fromtimestamp(int(last_message['internalDate']) // 1000)
                if last_date < from_datetime:
                    break

                # add next page if it exists
                time.sleep(1 / 40)
                request = messages.list(userId=self.email, includeSpamTrash=True, maxResults=500, pageToken=page['nextPageToken'], q='subject:[HARO]')
                page = request.execute()
                messages_list = messages_list + page['messages']
            
            # ensure only relevant HARO emails
            to_ret = list()
            found = False
            for mes in messages_list:
                # to not overrun rate limit of 50 calls per second
                time.sleep(1 / 40)
                request = messages.get(userId=self.email, id=mes['id'], format='full')
                message = request.execute()
                headers = message['payload']['headers']
                for dic in headers:
                    if dic['name'] == "Subject":
                        if "[HARO]" in dic['value'] and from_datetime <= datetime.date.fromtimestamp(int(message['internalDate']) // 1000):
                            found = True
                            haro_obj = Haro([message])
                            to_ret.append(haro_obj)
            if not found:
                service.close()
                print("NO HARO FOUND")
                return None
            service.close()
            return to_ret

        except HttpError as error:
            # TODO Handle errors from gmail API.
            print(f"An error occurred: {error}")
            print("NO HARO FOUND")

    # @params: haros: a list of message objects
    # @return: None
    def haros_to_json(self, haros : list):
        """A method for dumping a list of HARO email objects to an output json file
        
        input
        
        haros: a list of HARO email objects from google api"""
        if not os.path.exists('haro_jsons/'):
            os.mkdir('haro_jsons/')
        if len(haros) == 0:
            return None
        if len(haros) == 1:
            timestamp = datetime.datetime.fromtimestamp(int(haros[0]['internalDate']) // 1000)
            time_out = timestamp.isoformat(timespec='seconds')
            with open('haro_jsons/HARO' + time_out + '.json', 'w') as outfile:
                json.dump(haros, outfile, indent=4)
        else:
            from_time = datetime.datetime.fromtimestamp(int(haros[-1]['internalDate']) // 1000).isoformat(timespec='seconds')
            to_time = datetime.datetime.fromtimestamp(int(haros[0]['internalDate']) // 1000).isoformat(timespec='seconds')
            with open('haro_jsons/HARO' + from_time + 'TO' + to_time + '.json', 'w') as outfile:
                json.dump(haros, outfile, indent=4)



if __name__ == '__main__':
    # TODO can write to output file, or use with Chris's parser
    listener = HaroListener('chris@lightyearstrategies.com', False)
    test = listener.find_haro_from("2021-12-24")
    df_save = pd.DataFrame()
    for haro in test:
        df_save = df_save.append(haro.get_dataframe())
    df_save = df_save.reset_index(drop=True)
    df_save.to_csv('haro_jsons/HARO_test.csv')

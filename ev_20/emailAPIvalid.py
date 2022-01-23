import requests
import re
import pandas as pd
import os
import json


class emailValidation:
    def __init__(self, filename=None, key=None):
        if filename != None:
            self.type = filename.split('.')[-1]
            if self.type not in ['csv', 'xlsx']:
                raise Exception('File type not supported')
            else:
                self.filename = filename

        self.df = self.__get_df()
        self.key = key
        if (self.key is None):
            try:
                with open('key.json') as json_file:
                    data = json.load(json_file)
                    self.key = data
            except:
                print("No key.json file found")

        self.url = 'https://isitarealemail.com/api/email/validate'

    def __get_df(self):
        df = pd.DataFrame()
        try:
            if self.type == 'csv':
                df = pd.read_csv(self.filename)
            elif self.type == 'xlsx':
                df = pd.read_excel(self.filename)
        except:
            raise Exception('File not found')

        if "email" in df.columns:
            df.rename(columns={"email": "Email(s)"}, inplace=True)
        elif "Email(s)" in df.columns:
            pass
        elif "Email" in df.columns:
            df.rename(columns={"Email": "Email(s)"}, inplace=True)
        elif "Email " in df.columns:
            df.rename(columns={"Email ": "Email(s)"}, inplace=True)
        else:
            print(df.columns)
            raise Exception("Column not found")

        return df

    def set_key(self, key):
        self.key = key

    def check(self, email):
        try:
            if type(email) != str:
                return 'invalid'
            if (len(email) > 254 or len(email) < 3):
                return 'invalid'
            email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")
            if not email_regex.match(email):
                return 'invalid'
        except:
            return 'invalid'

        if self.key == None:
            response = requests.get(
                self.url,
                params={'email': email})
        else:
            response = requests.get(
                self.url,
                params={'email': email},
                headers={'Authorization': "Bearer " + self.key})
        return response.json()['status']

    def validation(self, save=False):
        data = self.df
        length = len(data)
        removed = 0

        for i in range(length):
            print(str(i) + '/' + str(length))
            if self.check(data["Email(s)"][i]) == 'invalid':
                data.drop(i, inplace=True)
                removed += 1
                print('Removed ' + str(removed) + ' invalid email(s)')

        self.df = data
        if save:
            self.to_cvs()

    def to_cvs(self):
        df = self.df
        df.to_csv(self.filename.split(".") + "_clean.csv", index=False)


if __name__ == '__main__':
    email = emailValidation(filename="test.csv")
    email.validation()

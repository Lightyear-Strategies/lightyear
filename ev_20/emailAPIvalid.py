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
        self.statistics = {
            'Initial Length': len(self.df)
        }
        self.wrong_emails = pd.DataFrame()

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
            if len(email) > 254 or len(email) < 3:
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

    def validation(self, save=False, stats=False, record_removed=False):
        self.__remove_duplicates()
        data = self.df
        length = len(data)
        removed = 0

        for i in range(length):
            percent = round((i / length) * 100,2)
            print(str(i) + '/' + str(length) + ' ' + str(percent) + '%')
            if self.check(data["Email(s)"][i]) == 'invalid':
                if record_removed:
                    self.wrong_emails = self.wrong_emails.append(
                        {'Email(s)': data["Email(s)"][i]}, ignore_index=True)

                data.drop(i, inplace=True)
                removed += 1
                print('Removed ' + str(removed) + ' invalid email(s)')
        self.statistics['Invalid Emails Removed'] = removed
        self.statistics['Final Length'] = len(data)
        self.df = data

        if stats:
            print(self.show_stats())
        if save:
            self.to_cvs()
        else:
            return self.df

    def __remove_duplicates(self):
        # Remove duplicates and count the number of duplicates
        df = self.df
        df.drop_duplicates(subset=['Email(s)'], keep='first', inplace=True)
        removed = len(df) - len(self.df)
        self.statistics['Duplicates Removed'] = removed
        self.df = df

    def to_cvs(self):
        df = self.df
        df.to_csv(self.filename.split(".")[0] + "_clean.csv", index=False)

    def show_stats(self):
        return self.statistics

    def show_wrong_emails(self):
        return self.wrong_emails


if __name__ == '__main__':
    email = emailValidation(filename="Pulse1.csv")
    email.validation(save=True)

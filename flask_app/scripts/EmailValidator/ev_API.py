import requests, re, os, json
import pandas as pd

from flask_app.scripts.config import Config


class emailValidation:
    def __init__(self, filename=None, key=None):
        if filename:
            self.type = filename.split('.')[-1]
            if self.type not in ['csv', 'xlsx']:
                raise Exception('File type not supported')
            else:
                self.filename = filename

        self.df = self.__get_df()
        self.key = key
        if (self.key is None):
            try:
                # with open(Config.EV_API_KEY) as json_file:
                #     data = json.load(json_file)
                #     self.key = data
                self.key = Config.EV_API_KEY
            except Exception as e:
                print(e)
                print("No ev_api_key.json in CONFIG_DIR file found")

        self.url = 'https://isitarealemail.com/api/email/validate'
        self.statistics = { 'Initial Length': len(self.df) }
        self.wrong_emails = pd.DataFrame()

    def __get_df(self):
        df = pd.DataFrame()
        try:
            if self.type == 'csv':
                df = pd.read_csv(self.filename)
            elif self.type == 'xlsx':
                df = pd.read_excel(self.filename)
        except Exception:
            raise Exception('File not found')

        for i in range(len(df.columns)):
            column_name = df.columns[i]
            if 'email' in column_name.lower():
                df.rename(columns={column_name: 'Email(s)'}, inplace=True)
                return df

        raise Exception('No email column found')

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
        except Exception:
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

        # Debugging
        # Important to remember to verify sufficient balance at https://isitarealemail.com/

        # print(response.json())
        # try:
        #     return response.json()['status']
        # except as Exception:
        #     pass

        return response.json()['status']

    def validation(self, save=False, stats=False, record_removed=False):
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

        #data.loc[-1] = 'Checked by Lightyear Strategies'

        self.statistics['Invalid Emails Removed'] = removed
        self.statistics['Final Length'] = len(data)
        self.df = data

        if stats:
            print(self.show_stats())
        if save:
            self.to_cvs()
        else:
            return self.df


    def to_cvs(self):
        filename = os.path.basename(self.filename)

        filename = os.path.join(Config.UPLOAD_DIR,filename)
        if os.path.exists(filename):
            os.remove(filename)
            print(f"The {filename} has been deleted successfully")
        else:
            print(f"The {filename} does not exist!")
        self.df.to_csv(path_or_buf=filename, index=False)

    def remove_duplicates(self, csv_file, save=False):
        df = pd.read_csv(csv_file)
        initial = len(df)
        df.drop_duplicates(subset=['Email(s)'], keep='first', inplace=True)
        removed = initial - len(df)
        #print(removed)
        if save:
            df.to_csv(csv_file.split(".")[0]+"final.csv", index=False)
        else:
            return df

    def show_stats(self):
        return self.statistics

    def show_wrong_emails(self):
        return self.wrong_emails


if __name__ == '__main__':
    email = emailValidation(filename="email_valid.csv")
    email.validation(save=True)


import json, os, base64
import pandas as pd
import haroListener.muckRack.google_muckrack as mc
from datetime import datetime

""""
Haro class

    Should be able to parse a haro file and return a pandas dataframe
    with the data.
    
    Attributes:
        json_string (str): The json string to be parsed
    
    Key methods:
        __init__: Initializes the class. Simply put it in a json string.
        load_json_file: Sets the json_string for the class.
        
    The rest of the methods are helper methods and will work by themselves.
"""


class Haro:
    def __init__(self, json_string=None):
        self.json_string = json_string
        self.date = None
        self.subject = None
        self.message = None
        self.df = pd.DataFrame()

        if self.json_string is not None:
            self.__main_checks()

        self.received = None
        self.edition = None

    def __str__(self):
        print_statement = "Haro instance\n"

        if self.json_string is not None:
            print_statement += self.subject + "\n"
            print_statement += self.date + "\n"
        else:
            print_statement += "JSON: None\n"

        return print_statement

    def __repr__(self):
        instance = "HARO("
        if self.json_string is not None:
            instance += ' '.join(self.date.split(" ")[1:5]) + ")"
        return instance

    def __main_checks(self):
        if self.json_string is None:
            print('No json string found')
            return
        if self.date is None:
            self.__parse_date()
        if self.subject is None:
            self.__parse_subject()
        if self.message is None:
            self.parse()

    def load_json_file(self, file_path):
        if not os.path.exists(file_path):
            print('File not found')
            return
        try:
            with open(file_path) as f:
                self.json_string = json.load(f)
                self.__main_checks()
        except Exception as e:
            print('Invalid json')
            print(e)
            return

    def set_json_string(self, json_string):
        self.json_string = json_string

    def parse(self):
        try:
            #print(self.json_string[0]['payload']['parts'][0]['parts'])
            parsing_body = (self.json_string[0]['payload']['parts'][0]['parts'])
            #print('Fine')

            data = ""
            for part in range(len(parsing_body)):
                data += parsing_body[part]['body']['data']

            # decode base64
            data = base64.urlsafe_b64decode(data)
            data = data.decode('utf-8')
            # split lines
            split = data.split("****************************")

            # For some reason, shorter messages are not split correctly.
            if len(split) == 2:
                quarries = split[-1].split("-----------------------------------")[:-2]
            else:
                quarries = split[1].split("-----------------------------------")[:-3]

            self.message = quarries
            for m in self.message:
                self.__parse_help(m)
        except KeyError as ke:
            print('Error is related to',ke)


    def __parse_date(self):
        parsing_body = (self.json_string[0]['payload']['headers'])
        self.date = parsing_body[1]['value'].split(";")[-1].strip()

    def __parse_subject(self):
        parsing_body = (self.json_string[0]['payload']['headers'])
        self.subject = parsing_body[17]['value']

    def get_dataframe(self):
        return self.df

    def get_message(self):
        return self.message

    def get_subject(self):
        return self.subject

    def get_date(self):
        return self.date

    def format_date(self):
        temp = self.date.split(" ")[1:4]
        temp = temp[1] + " " + temp[0] + " " + temp[2]
        temp = datetime.strptime(temp, "%b %d %Y")
        self.received = temp.strftime("%Y-%m-%d")

    def save_dataframe(self, file_path, file_name):
        if(file_name[-4:] != ".csv" or file_name[-4:] != ".xlsx"):
            file_name += ".csv"
        if(file_path[-1:] != "/"):
            file_path += "/"

        df = self.get_dataframe()
        path = file_path+file_name+".csv"
        df.to_csv(path, index=False)

    def __parse_help(self, message):
        row_dict = dict()
        self.format_date()
        row_dict["Summary"] = message.split("Summary:")[-1].split("\n")[0].replace("\r", "").strip()
        row_dict["Name"] = message.split("Name:")[-1].split("\n")[0].replace("\r", "").strip()
        row_dict["Category"] = message.split("Category:")[-1].split("\n")[0].replace("\r", "").strip()
        row_dict["Email"] = message.split("Email:")[-1].split("\n")[0].replace("\r", "").strip()
        row_dict["MediaOutlet"] = message.split("Media Outlet:")[-1].split("\n")[0].replace("\r", "").strip()
        row_dict["Deadline"] = message.split("Deadline:")[-1].split("\n")[0].replace("\r", "").strip()
        row_dict["Query"] = message.split("Query:")[-1].split("Requirements:")[0].replace("\r", "").replace("\n", "").strip()
        row_dict["Requirements"] = message.split("Requirements:")[-1].replace("\r", "").replace("\n", "").strip()
        row_dict["DateReceived"] = self.received
        row_dict["Used"] = "None"
        row_dict["TimeStamp"] = datetime.fromisoformat(self.received).timestamp()
        self.df = self.df.append(row_dict, ignore_index=True)

    def parse_MC(self):
        df = self.df
        muckrack = mc.google_muckrack(df, "Name")
        result = muckrack.get_dataframe()


if __name__ == "__main__":
    test = Haro()
    test.load_json_file("haro_jsons/test.json")



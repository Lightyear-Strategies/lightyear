import json
import os
import base64
import pandas as pd

class Haro():
    def __init__(self, json_string=None):
        self.json_string = json_string
        self.date = None
        self.subject = None
        self.message = None
        self.df = pd.DataFrame()

        if(self.json_string is not None):
            self.__main_checks()

    def __str__(self):
        print_statement = "Haro instance\n"

        if(self.json_string is not None):
            print_statement += self.subject + "\n"
            print_statement += self.date + "\n"
        else:
            print_statement += "JSON: None\n"

        return print_statement

    def __repr__(self):
        instance = "HARO("
        if(self.json_string is not None):
            instance += ' '.join(self.date.split(" ")[1:5])+");"
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
        #parse json
        try:
            with open(file_path) as f:
                self.json_string = json.load(f)
                self.__main_checks()
        except:
            print('Invalid json')
            return

    def set_json_string(self, json_string):
        self.json_string = json_string

    def parse(self):
        parsing_body = (self.json_string[0]['payload']['parts'][0]['parts'])

        data = ""
        for part in range(len(parsing_body)):
            data+=parsing_body[part]['body']['data']

        #decode base64
        data=base64.urlsafe_b64decode(data)
        #break into lines
        data=data.decode('utf-8')
        #split lines based on "-----------------------------------"
        test = data.split("****************************")

        if(len(test)==2):
            quarries = test[-1].split("-----------------------------------")[:-2]
        else:
            quarries = test[1].split("-----------------------------------")[:-3]

        self.message = quarries
        for m in self.message:
            self.__parse_help(m)

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

    def __parse_help(self, message):
        dict = {}
        dict["Summary"] = message.split("Summary:")[-1].split("\n")[0].replace("\r","")
        dict["Name"] = message.split("Name:")[-1].split("\n")[0].replace("\r","")
        dict["Category"] = message.split("Category:")[-1].split("\n")[0].replace("\r","")
        dict["Email"] = message.split("Email:")[-1].split("\n")[0].replace("\r","")
        dict["Media Outlet"] = message.split("Media Outlet:")[-1].split("\n")[0].replace("\r","")
        dict["Deadline"] = message.split("Deadline:")[-1].split("\n")[0].replace("\r","")
        dict["Query"]=message.split("Query:")[-1].split("Requirements:")[0].replace("\r","").replace("\n","")
        dict["Requirements"] = message.split("Requirements:")[-1].replace("\r","").replace("\n","")
        self.df = self.df.append(dict, ignore_index=True)


if __name__ == "__main__":
    test = Haro()
    test.load_json_file("haro_jsons/test.json")

    print(test)
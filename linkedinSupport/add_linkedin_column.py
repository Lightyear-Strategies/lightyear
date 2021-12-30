"""a module to add a linkedin url to a spreadsheet"""

import os.path
import time
import random

from linkedin_api import Linkedin
import pandas as pd

class LinkedinAdder():
    """a class wrapper for the module"""

    # @params: email: the email you want to use to validate. Must be associated with a linkedin account, password: linkedin password
    # @returns: a linkedinadder object
    def __init__(self, email : str, password : str, debug : bool = False):
        """constructor for LinkedinAdder class
        
        input
        email: a string of the linkedin email you want to use to validate
        password: corresponding password"""
        self.email = email 
        self.password = password
        self.debug = debug
        self.api = Linkedin(email, password)

    
    # @params: sheet: a string path to a csv or xlsx
    # @return: a pandas dataframe with the added column
    def add_column(self, sheet : str):
        """a method to add a column of linkedin urls to a spreadsheet and return a pandas dataframe
        
        input
        sheet: a string filepath to a csv or xlsx"""

        if not os.path.exists(sheet):
            print("INVALID FILEPATH")
            return None

        extension = sheet.split('.')[-1]
        df = None

        if extension == 'csv':
            df = pd.read_csv(sheet)
        elif extension == 'xlsx':
            df = pd.read_excel(sheet)
        else:
            print("INVALID FILE EXENSION")
            return None

        if self.debug:
            print("BEFORE ADD")
            print(df)

        if len(df) > 100:
            df['linkedin url'] = df.apply(lambda row : self.__get_url(row['First Name'], row['Last Name'], True), axis=1)
        else:
            df['linkedin url'] = df.apply(lambda row : self.__get_url(row['First Name'], row['Last Name'], False), axis=1)

        if self.debug:
            print("\nAFTER ADD")
            print(df)

        return df

    # @params: first: str first name, last: str last name, big_df: bool if input large
    # @returns: a string url representing the linkedin account of "first last"
    def __get_url(self, first : str, last : str, big_df : bool):
        """a helper method to get the linkedin url of a person with a random waiting period to not get banned by linkedin
        
        input
        first: a string first name
        last: a string last name
        big_df: a boolean to tell whether the input is large (> 100 entries)"""

        # trying to trick linkedin
        if big_df:
            if random.randint(1, 100) == 50:
                # add big wait period for large input to not get killed by linkedin
                time.sleep(random.randint(600, 1000))
        time.sleep(random.randint(3, 18))

        keywords = f"{first} {last} Journalist"
        users_list = self.api.search_people(keywords=keywords)

        if self.debug:
            print(users_list)
        
        if len(users_list) == 0:
            return "N/A"

        return "linkedin.com/in/" + users_list[0]['public_id'] + "/"


    # @params: sheet: str filepath
    # @returns: None
    def add_connections(self, sheet : str):
        """a method to take a sheet of journalists WITH LINKEDIN URLS and connect with them, 50 at a time (50 per 24 hours)
        
        input
        sheet: string filepath to spreadsheet"""

        if not os.path.exists(sheet):
            print("INVALID FILEPATH")
            return None

        extension = sheet.split('.')[-1]
        df = None

        if extension == 'csv':
            df = pd.read_csv(sheet)
        elif extension == 'xlsx':
            df = pd.read_excel(sheet)
        else:
            print("INVALID FILE EXENSION")
            return None
        
        if len(df) > 50:
            num_pieces = (len(df) // 50) + 1
            pieces = [df[i * 50 : (i + 1) * 50] for i in range(num_pieces)]
            for tmp_df in pieces:
                tmp_df.apply(lambda row : self.__add_connection(row), axis=1)
                # so that our account does not get banned
                time.sleep(504000)
        else:
            df.apply(lambda row : self.__add_connection(row), axis=1)

    # @params: url: row: row of df
    # @returns: None
    def __add_connection(self, row):
        """a helper method to add a single connection with personalized message
        
        input
        row: row of dataframe"""
        # personalized message
        message = self.__write_message(row)
        # id from url
        pub_id = self.__get_id(row)
        self.api.add_connection(profile_public_id=pub_id, message=message)
        time.sleep(random.randint(600, 1200))

    # @params: row: row of df
    # @returns: a personalized message
    # TODO: IMPLEMENT THIS
    def __write_message(self, row):
        """a helper method to take a row of a dataframe and return a personalized message to the client
        
        input
        row: row of dataframe"""
        raise NotImplementedError

    # @params: row: row of df
    # @returns: a linkedin public id
    def __get_id(self, row):
        """a helper method to take a row of a dataframe and return a linkedin public id
        
        input
        row: row of dataframe"""
        return row['linkedin url'].split('/')[-2]

if __name__ == '__main__':
    if not os.path.exists('config/'):
        print("please make a folder named 'config/' containing the files 'email.txt' with just the linkedin email address and 'password.txt' with just the password")
        exit()
    with open('config/email.txt') as email, open('config/password.txt') as password:
        un = email.read()
        pw = password.read()
        adder = LinkedinAdder(un, pw, False)
        # DO NOT EDIT ABOVE HERE. IMPORTANT FOR CONFIGURATION

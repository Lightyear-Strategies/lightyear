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
        """a method to add a column of linkedin urls to a spreadsheet
        
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

        df['linkedin url'] = df.apply(lambda row : self.__get_url(row['First Name'], row['Last Name']), axis=1)

        if self.debug:
            print("\nAFTER ADD")
            print(df)

        return df

    # @params: first: str first name, last: str last name
    # @returns: a string url representing the linkedin account of "first last"
    def __get_url(self, first : str, last : str):
        """a helper method to get the linkedin url of a person with a random waiting period to not get banned by linkedin
        
        input
        first: a string first name
        last: a string last name"""

        # trying to trick linkedin
        time.sleep(random.randint(3, 18))

        users_list = self.api.search_people(keyword_first_name=first, keyword_last_name=last)

        if self.debug:
            print(users_list)
        
        profile_dict = self.api.get_profile(users_list[0]['public_id'], users_list[0]['urn_id'])

        if self.debug:
            print(profile_dict)

        return "linkedin.com/in/" + users_list[0]['public_id'] + "/"

if __name__ == '__main__':
    if not os.path.exists('config/'):
        print("please make a folder named 'config/' containing the files 'email.txt' with just the linkedin email address and 'password.txt' with just the password")
        exit()
    with open('config/email.txt') as email, open('config/password.txt') as password:
        un = email.read()
        pw = password.read()
        adder = LinkedinAdder(un, pw, False)
        # DO NOT EDIT ABOVE HERE. IMPORTANT FOR CONFIGURATION
        print(adder.add_column('config/minitest.csv'))
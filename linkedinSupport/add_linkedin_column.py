"""a module for linkedin outreach automation"""

import os.path
import time
import random
import base64

from linkedin_api import Linkedin
import pandas as pd
import numpy as np

class my_Linkedin(Linkedin):
    """a wrapper for the linkedin api that contains the add_connection functionality"""

    def __init__(self, username, password):
        super().__init__(username, password)

    def generateTrackingId(self):
        """Generates and returns a random trackingId
        :return: Random trackingId string
        :rtype: str
        """
        random_int_array = [random.randrange(256) for _ in range(16)]
        rand_byte_array = bytearray(random_int_array)
        return str(base64.b64encode(rand_byte_array))[2:-1]

    def add_connection(self, profile_public_id, message="", profile_urn=None):
        """Add a given profile id as a connection.
        :param profile_public_id: public ID of a LinkedIn profile
        :type profile_public_id: str
        :param message: message to send along with connection request
        :type profile_urn: str, optional
        :param profile_urn: member URN for the given LinkedIn profile
        :type profile_urn: str, optional
        :return: Error state. True if error occurred
        :rtype: boolean
        """

        # Validating message length (max size is 300 characters)
        if len(message) > 300:
            self.logger.info("Message too long. Max size is 300 characters")
            return False

        if not profile_urn:
            profile_urn_string = self.get_profile(public_id=profile_public_id)[
                "profile_urn"
            ]
            # Returns string of the form 'urn:li:fs_miniProfile:ACoAACX1hoMBvWqTY21JGe0z91mnmjmLy9Wen4w'
            # We extract the last part of the string
            profile_urn = profile_urn_string.split(":")[-1]

        trackingId = self.generateTrackingId()
        payload = (
            '{"trackingId":"'
            + trackingId
            + '", "message":"'
            + message
            + '", "invitations":[], "excludeInvitations":[],"invitee":{"com.linkedin.voyager.growth.invitation.InviteeProfile":\
            {"profileId":"'
            + profile_urn
            + '"'
            + "}}}"
        )
        res = self._post(
            "/growth/normInvitations",
            data=payload,
            headers={"accept": "application/vnd.linkedin.normalized+json+2.1"},
        )

        return res.status_code != 201

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
        self.api = my_Linkedin(email, password)

    def __get_haro_url(self, row, big_df : bool):
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

        name = row['Name']

        if name == np.nan or name == np.NaN or type(name) == float:
            return "N/A"

        name = name.strip()

        # cases for finding journalists, best to worst
        outlet = row['MediaOutlet']

        if outlet != None:
            # best search results
            keywords = f"{name} {outlet}"
        else:
            # significantly worse performance
            keywords = f"{name} Journalist"

        users_list = self.api.search_people(keywords=keywords)

        if len(users_list) == 0:
            if self.debug:
                print("couldnt find")
            return "N/A"

        if self.debug:
            print(users_list)

        return "linkedin.com/in/" + users_list[0]['public_id'] + "/"

    def add_column_haro(self, df : pd.DataFrame):
        """
        a method to take the database and add linkedin urls
        
        input
        
        df : a pandas DataFrame of the database
        """
        if self.debug:
            print("BEFORE ADD")
            print(df)

        if len(df) > 100:
            df['linkedin url'] = df.apply(lambda row : self.__get_haro_url(row, True), axis=1)
        else:
            df['linkedin url'] = df.apply(lambda row : self.__get_haro_url(row, False), axis=1)

        if self.debug:
            print("\nAFTER ADD")
            print(df)

        return df



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
            df['linkedin url'] = df.apply(lambda row : self.__get_url(row, True), axis=1)
        else:
            df['linkedin url'] = df.apply(lambda row : self.__get_url(row, False), axis=1)

        if self.debug:
            print("\nAFTER ADD")
            print(df)

        return df

    # @params: first: str first name, last: str last name, big_df: bool if input large
    # @returns: a string url representing the linkedin account of "first last"
    def __get_url(self, row, big_df : bool):
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

        first = row['First Name']
        last = row['Last Name']

        if first == np.nan or last == np.nan or first == np.NaN or last == np.NaN or type(first) == float or type(last) == float:
            return "N/A"

        first = row['First Name'].strip()
        last = row['Last Name'].strip()

        # cases for finding journalists, best to worst
        outlet = self.__get_top_outlet(row)

        if outlet != None:
            # best search results
            keywords = f"{first} {last} {outlet}"
        else:
            # significantly worse performance
            keywords = f"{first} {last} Journalist"

        users_list = self.api.search_people(keywords=keywords)

        if len(users_list) == 0:
            if self.debug:
                print("couldnt find")
            return "N/A"

        if self.debug:
            print(users_list)

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

        if message == "":
            print(f"COULD NOT ADD {row['First Name']} {row['Last Name']}: BAD NAME OR OUTLET")
            return
        # id from url
        if type(row['linkedin url']) == float:
            print("NO LINKEDIN URL COULD BE FOUND")
            return 

        pub_id = self.__get_id(row)


        if self.debug:

            print(f"MESSAGE: {message}\nID: {pub_id}")
            print("CONNECTION NOT ADDED, DEBUGGING")
            exit()

        self.api.add_connection(profile_public_id=pub_id, message=message)
        time.sleep(random.randint(600, 900))

    # @params: row: row of df
    # @returns: a personalized message
    def __write_message(self, row):
        """a helper method to take a row of a dataframe and return a personalized message to the client
        
        input
        row: row of dataframe"""

        greeting_choices = ["Hi", "Hello", "Greetings"]
        butter_choices = ["I really enjoyed", "I really loved", "I loved", "I enjoyed reading"]
        work_choices = ["all your work", "the work you've done", "your contributions"]
        connection_choices = ["Let's connect", "I'd like to connect"]
        help_choices = ["how we could potentially help each other", "potentially working together", "how we may be able to help each other out"]

        greeting = random.choice(greeting_choices)
        butter = random.choice(butter_choices)
        work = random.choice(work_choices)
        connection = random.choice(connection_choices)
        help_c = random.choice(help_choices)
        
        if row['First Name'] == np.NaN or row['Last Name'] == np.NaN or row['First Name'] == np.nan or row['Last Name'] == np.nan or type(row['First Name']) == float or type(row['Last Name']) == float:
            return ""

        first = row['First Name'].strip()

        outlet_choice = self.__get_top_outlet(row)

        if outlet_choice == None:
            message = f"{greeting} {first}. {butter} some of your freelance work. {connection} and talk about {help_c}."

            if self.debug:
                print(message)
            
            return message
        
        message = f"{greeting} {first}. {butter} {work} at {outlet_choice}. {connection} and talk about {help_c}."

        if self.debug:
            print(message)
        
        return message
                
    # @params: row: row of df
    # @returns: a linkedin public id
    def __get_id(self, row):
        """a helper method to take a row of a dataframe and return a linkedin public id
        
        input
        row: row of dataframe"""
        return row['linkedin url'].split('/')[-2] # grabs just public id from url

    # @params: row: row of df
    # @returns: a string representation of the reporter's top outlet
    def __get_top_outlet(self, row):
        """a helper method to take a row of a dataframe and return a string indicating the most popular outlet
        
        input
        row: row of dataframe"""
        first = row['First Name'].strip()
        last = row['Last Name'].strip()
        outlet_list = [out.strip() for out in row['Outlet(s)'].split(',')]
        for out in outlet_list:
            if out == np.nan or out == np.NaN:
                return None
            if first not in out and last not in out:
                return out
        return None

if __name__ == '__main__':
    if not os.path.exists('config/'):
        print("please make a folder named 'config/' containing the files 'email.txt' with just the linkedin email address and 'password.txt' with just the password")
        exit()
    with open('config/email.txt') as email, open('config/password.txt') as password:
        un = email.read()
        pw = password.read()
        adder = LinkedinAdder(un, pw, True) # IN DEBUG MODE, USE FALSE OPTION FOR PRODUCTION
        # DO NOT EDIT ABOVE HERE. IMPORTANT FOR CONFIGURATION
        # if adder.debug:
        #     print(pd.read_csv('config/minitest.csv')[['First Name', 'Last Name', 'Outlet(s)']])
        # to_write = adder.add_column("config/minitest.csv")
        # with open("config/minitest_with_linkedin.csv", "w") as outfile:
        #     to_write.to_csv(outfile)
        # adder.add_connections("config/minitest_with_linkedin.csv")
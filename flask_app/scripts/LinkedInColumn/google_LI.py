from googlesearch import search
import pandas as pd
import time
import random

class linked_in_search:
    def __init__(self, dataframe):
        self.df = dataframe #init the dataframe
        self.colname = self.__find_column()
        self.wait = 1

        if(self.colname == -1):
            raise Exception("Column Name or Full Name not found")


    def __find_column(self):
        """ Looks for the columns NAME or FULL NAME in the dataframe and returns the column name for __init__"""
        for col in self.df.columns:
            if col == "Name" or col == "Full name":
                return col
        return -1


    def __column_iterate(self, debug=False):
        """ Iterates through the column and calls __lookUp() for each row """
        for index, row in self.df.iterrows():
            if(debug):
                total = len(self.df)
                print("{}/{}".format(index, total))

            name = row[self.colname]
            url = self.__lookUp(name, debug)
            self.df.at[index, "LinkedIn"] = url
            self.save_dataframe("LinkedIN_incomplete.csv") #save the progress of the program


    def get_dataframe(self):
        return self.df


    def initiate_search(self, debug=False, pause=1):
        self.__column_iterate(debug)
        self.wait = pause


    def save_dataframe(self, filename):
        self.df.to_csv(filename)


    def __lookUp(self, name, debug=False):
        if not isinstance(name, str):
            return 'ERROR'
        if name == '' or len(name) < 3:
            return 'No name given'

        if debug:
            print("Searching for {}".format(name))

        query = name + " " + "linkedin"

        tries_left = 3
        request_speed_issue = False

        while tries_left > 0:
            try:
                s = list(search(query, num=1, stop=1, pause=self.wait))[0]
                if "linkedin.com" not in s:
                    if(debug):
                        print("Not a linkedin profile found")
                    return None
                elif "linkedin.com" in s:
                    if(debug):
                        print("Linkedin profile found")
                    if(self.wait > 1): #Slowly reducing the wait time after successful requests
                        self.wait -= 0.1
                    return s
            except Exception as e: #Handle the 429 error
                if(debug):
                    print("Error: " + str(e))
                if("HTTP Error 429" in str(e)):
                    waiting_time = random.randint(self.wait*45,self.wait*60)
                    if(debug):
                        print("Waiting for {} seconds".format(waiting_time))
                        print("Tries left: {}".format(tries_left))
                        print("Current wait: {} seconds".format(self.wait))
                    time.sleep(waiting_time)
                    request_speed_issue = True
                continue
        if(request_speed_issue):
            self.wait += 1
            if(debug):
                print("Request wait time increased")
                print("Current wait: {} seconds".format(self.wait))
            return "HTTP Error 429"
        return "ERROR"


if __name__ == '__main__':
    df = pd.read_csv("holaplex.csv")
    linkedin = linked_in_search(df)
    linkedin.initiate_search(debug=True, pause=1)
    linkedin.save_dataframe("holaplex_LI.csv")

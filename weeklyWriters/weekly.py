import pandas as pd
from muckRack import Muckrack as MC
from muckRack import google_muckrack as gm

#To-do:
#1) Go through the list of authors and get their muckrack links
#1.5) Optionally, use the existing links to analyze the data
#2) Gather the most recent articles, gather the key words, gather media outlets
#3) Create a dataframe with the data

class WeeklyReport:
    def __init__(self, filename, colname, parsed=False):
        self.filename = filename
        self.colname = colname
        self.df = self.__parse_df(self.filename)
        if parsed == False:
            self.add_muckrack()


    def __parse_df(self, filename):
        try:
            df = pd.read_csv(filename)
            return df
        except:
            print("Error: File not found")
            return None

    def add_muckrack(self):
        look_up = gm.google_muckrack(self.df, self.colname)
        self.df = look_up.get_dataframe()
        #REMOVE LATER ON
        self.df.to_csv("test_out.csv")

    def muckrack_analysis(self):
        #convert self.df["Muckrack"] to a list
        list = self.df["Muckrack"].tolist()
        mc = MC.Muckrack(list)
        mc.parse_HTML()
        mc.save_to_csv("muckrack_analysis.csv")


    def get_dataframe(self):
        return self.df








if __name__ == "__main__":
    df = WeeklyReport("liams_test.csv", "Name", parsed=False)
    df.muckrack_analysis()

import pandas as pd
from muckRack import Muckrack as MC
from muckRack import google_muckrack as gm

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

    def muckrack_analysis(self):
        list = self.df["Muckrack"].tolist()
        mc = MC.Muckrack(list)
        mc.parse_HTML()
        mc.save_to_csv("muckrack_analysis.csv")


    def get_dataframe(self):
        return self.df


if __name__ == "__main__":
    df = WeeklyReport("test.csv", "Name")
    df.muckrack_analysis()


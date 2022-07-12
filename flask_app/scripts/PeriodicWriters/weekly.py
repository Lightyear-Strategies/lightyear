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
            raise Exception("File not found")

    def add_muckrack(self):
        look_up = gm.google_muckrack(self.df, self.colname)
        look_up.save_dataframe(self.filename)
        self.df = look_up.get_dataframe()

    def muckrack_analysis(self):
        list = self.df["Muckrack"].tolist()
        mc = MC.Muckrack(url_list=list)
        mc.parse_HTML()
        mc.save_to_csv("muckrack_analysis.csv")


    def get_dataframe(self):
        return self.df


if __name__ == "__main__":
    df = WeeklyReport("journalists/top50Economics.csv", "Name", parsed=True)
    df.muckrack_analysis()
    #df.muckrack_analysis()


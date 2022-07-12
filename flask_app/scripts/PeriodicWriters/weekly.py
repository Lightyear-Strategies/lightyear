import pandas as pd
import os
from muckRack import Muckrack as MC
from muckRack import google_muckrack as gm
from toPDF import pdfReport as pdf

class Report:
    #INNER METHODS
    def __init__(self, filename=None, colname=None, parsed=False):
        self.filename = filename
        self.colname = colname
        if(filename is not None):
            self.df = self.__parse_df(filename)

        if parsed == False:
            self.add_muckrack()

        self.analyzed = None

    def __parse_df(self, filename):
        try:
            df = pd.read_csv(filename)
            return df
        except:
            raise Exception("File not found")

    #ANALYSIS METHODS
    def add_muckrack(self):
        look_up = gm.google_muckrack(self.df, self.colname)
        look_up.save_dataframe(self.filename)
        self.df = look_up.get_dataframe()

    def muckrack_analysis(self):
        list = self.df["Muckrack"].tolist()
        mc = MC.Muckrack(url_list=list)
        mc.parse_HTML()
        result = mc.get_dataframe()
        self.analyzed = result

    def parse_category(self, category):
        csvname = {
            "AI": "top50AI.csv",
            "Crypto": "top50Crypto.csv",
            "Economics": "top50Economics.csv",
            "Marketing": "top50Marketing.csv",
            "NFT": "top50NFT.csv",
            "Philosophy": "top50Philosophy.csv",
            "test": "test.csv"
        }
        filename = "journalists/" + csvname[category]
        r = Report(filename, "Name", True)
        r.muckrack_analysis()
        pdf_filename = "reports/" + csvname[category].replace(".csv", ".pdf")
        r.convert_to_pdf(pdf_filename)

    def parse_all_categories(self):
        list_of_categories = ["AI", "Crypto", "Economics", "Marketing", "NFT", "Philosophy"]
        for category in list_of_categories:
            self.parse_category(category)

    #GET METHODS
    def get_dataframe(self):
        return self.df

    def get_analyzed_result(self):
        return self.analyzed

    #SAVE METHODS
    def save_analyzed_result(self, filename):
        if(self.analyzed is None):
            raise Exception("No analyzed result")
        self.analyzed.to_csv(filename)

    def convert_to_pdf(self, filename):
        result = pdf(df=self.analyzed)
        result.create_PDF(filename)



if __name__ == "__main__":
    df = Report(parsed=True)
    df.parse_category("NFT")


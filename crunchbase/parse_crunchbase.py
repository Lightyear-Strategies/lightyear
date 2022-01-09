"""a module to scrape crunchbase website without using our crunchbase credits"""

import time
import random as r 

import pandas as pd
import undetected_chromdriver as uc
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options

class CrunchParse():
    """a class wrapper for our script"""

    def __init__(self, un : str, pw : str, debug : bool = False):
        """constructor for CrunchParse class
        
        input
        un: a string username (likely Nima's username)
        pw: a string password (likely Nima's also)
        debug: do you want to debug ??
        """
        self.un = un 
        self.pw = pw 
        self.debug = debug
        self.companies_df = pd.DataFrame()

    # TODO: make keyword options instead of dict for easier gui implementation
    def parse(self, options : dict = None):
        """parses the table that crunchbase generates based on specific parameters
        
        input
        options: a dict containing the options and their values
        """
        # driver set up
        chrome_options = Options()
        #chrome_options.add_argument("--disable-extensions") # OPTIONAL
        #chrome_options.add_argument("--disable-gpu") # NECESSARY for windows
        #chrome_options.add_argument("--no-sandbox") # NECESSARY for linux
        #chrome_options.add_argument("--headless") # NECESSARY for all platforms
        driver = webdriver.Chrome()
        driver.get("https://www.crunchbase.com/discover/organization.companies") # go straight to crunchbase advanced search
        while True:
            pass
if __name__ == "__main__":
    CrunchParse("unknown", "unknown", True).parse()
    
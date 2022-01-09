"""a module to scrape crunchbase website without using our crunchbase credits"""

import time
import random as r 

import pandas as pd
import undetected_chromedriver as uc
from bs4 import BeautifulSoup

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
        self.driver = uc.Chrome()
    
    def __login(self):
        """a helper method to log the user in using the username and password instance variables
        
        input
        
        None
        """
        # go to login page that redirects to advanced search
        self.driver.get(r"https://www.crunchbase.com/login?redirect_to=%2Fdiscover%2Forganization.companies")
        time.sleep(5)

        email_form = self.driver.find_element_by_name("email")
        pass_form = self.driver.find_element_by_name("password")
        email_form.send_keys(self.un)
        time.sleep(1.63478)
        pass_form.send_keys(self.pw)
        time.sleep(1.232)
        self.driver.find_element_by_xpath('//*[@id="mat-tab-content-0-0"]/div/login/form/button').click()
        time.sleep(3)
        self.driver.refresh()

    # TODO: make keyword options instead of dict for easier gui implementation
    def parse(self, options : dict[str, str] = None):
        """parses the table that crunchbase generates based on specific parameters
        
        input

        options: a dict containing the options and their values
        """
        pass

if __name__ == "__main__":
    CrunchParse("unknown", "unknown", True).parse()
    
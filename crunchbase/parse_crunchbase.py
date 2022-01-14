"""a module to scrape crunchbase website without using our crunchbase credits"""

import time

import pandas as pd
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys

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
    
    def login(self):
        """a helper method to log the user in using the username and password instance variables
        
        input
        
        None
        """
        # go to login page that redirects to advanced search
        self.driver.get(r"https://www.crunchbase.com/login?redirect_to=%2Fsearch%2Ffunding_rounds")
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
    def parse(self):
        """parses the table that crunchbase generates based on specific parameters
        
        input

        options: a dict containing the options and their values
        """
        
        # THIS IS FOR DISCOVERY, NOT QUERY BUILDER. NOT FOR USE RIGHT NOW

        # map_options = {"overview" : 1, "contacts" : 2, "signals" : 3, "financials" : 4, "company status" : 5, "notes, lists, tags" : 6, "partner filters" : 7}

        # xpath = lambda option : f"/html/body/chrome/div/mat-sidenav-container/mat-sidenav-content/div/discover/page-layout/div/div/div[2]/section[1]/div[1]/mat-accordion/mat-expansion-panel[{map_options[option]}]"

        # # make everything uniform
        # self.driver.find_element_by_xpath(xpath("overview")).click()
        # time.sleep(2)

        # # activate filters
        # possible_filters = map_options.keys()

        # for filter_group in options.keys():
        #     if filter_group not in possible_filters:
        #         print("BAD FILTER GROUP NAME, QUITTING")
        #         self.driver.quit()
        #         exit()
        #     if options[filter_group] == None:
        #         continue
        #     self.driver.find_element_by_xpath(xpath(filter_group)).click()
        #     time.sleep(1.2382)


            
    def __anounced_date_option(self, date):
        # date in format mm/dd/yyyy
        self.driver.find_element_by_xpath('/html/body/chrome/div/mat-sidenav-container/mat-sidenav-content/div/search/page-layout/div/div/form/div[1]/div/filters/query-item-add/div/button')
        time.sleep(3)
        mini_window = self.driver.find_element_by_xpath('//*[@id="mat-input-7"]')
        mini_window.send_keys("announced date")
        time.sleep(0.54)
        mini_window.send_keys(Keys.ENTER)
        time.sleep(3)
        self.driver.find_element_by_xpath('//*[@id="mat-input-14"]').send_keys(date)
        time.sleep(4)
        self.driver.find_element_by_xpath('//*[@id="mat-input-14"]').send_keys(Keys.ENTER)

    def __in_location_option(self, location):
        self.driver.find_element_by_xpath('/html/body/chrome/div/mat-sidenav-container/mat-sidenav-content/div/search/page-layout/div/div/form/div[1]/div/filters/div/div/div/query-item/div/predicate/div/div[1]/query-item-add/div/button').click()
        time.sleep(3)
        mini_window = self.driver.find_element_by_xpath('//*[@id="mat-input-7"]')
        mini_window.send_keys("location")
        time.sleep(0.54)
        mini_window.send_keys(Keys.ENTER)
        time.sleep(3)
        self.driver.find_element_by_xpath('//*[@id="mat-input-8"]').send_keys(location)
        time.sleep(0.453)
        self.driver.find_element_by_xpath('//*[@id="mat-option-159"]')

if __name__ == "__main__":
    pass    
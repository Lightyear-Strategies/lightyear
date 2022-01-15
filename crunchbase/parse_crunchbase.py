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
        time.sleep(5)


    def add_option(self, option : str):
        """
        a method to add an option to the query builder on crunchbase. MUST be run AFTER login()
        
        input
        
        option : string representing the name of the option you want to add
        """
        self.driver.find_element_by_xpath('/html/body/chrome/div/mat-sidenav-container/mat-sidenav-content/div/search/page-layout/div/div/form/div[1]/div/filters/query-item-add/div/button')
        time.sleep(3)
        mini_window = self.driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/mat-dialog-container/query-item-drill-panel/div/dialog-layout/div/mat-dialog-content/div/div/div[1]/div/div/panel-search-input/mat-form-field/div/div[1]/div[4]/input"]')
        mini_window.send_keys(option)
        time.sleep(0.54)
        mini_window.send_keys(Keys.ENTER)
        time.sleep(3)
            
    def add_anounced_date(self, date : str):
        """
        a method to add the "after announced date" option to the field. MUST be run AFTER adding the option with add_option("announced date") and BEFORE adding any other options
        
        input
        
        date: a string representing the date
        """
        self.driver.find_element_by_xpath('/html/body/chrome/div/mat-sidenav-container/mat-sidenav-content/div/search/page-layout/div/div/form/div[1]/div/filters/div/div/div/query-item/div/predicate/div/div[2]/values/div/search-date/div/span/text-input/div/mat-form-field/div/div[1]/div/input').send_keys(date)
        time.sleep(4)

    def add_location(self, location : str):
        """
        a method to add a location to the field. MUST be run AFTER adding the option with add_option("location") and AFTER adding the announced date with add_announced_date
        
        input
        
        location: a string representing the location
        """
        self.driver.find_element_by_xpath('/html/body/chrome/div/mat-sidenav-container/mat-sidenav-content/div/search/page-layout/div/div/form/div[1]/div/filters/div/div/div[2]/query-item/div/predicate/div/div[2]/values/div/search-identifier/div/multi-entity-input/div/entity-input/mat-form-field/div/div[1]/div[2]/input').send_keys(location)
        time.sleep(1.454)
        self.driver.find_element_by_xpath('/html/body/div[5]/div/div/div/mat-option[1]').click()
        time.sleep(3)

    def not_in_location_option(self):
        """a method to change the location from "includes" to "does not include". MUST be run AFTER adding any locations with add_location(location)
        
        input
        
        None
        """
        self.driver.find_element_by_xpath('/html/body/chrome/div/mat-sidenav-container/mat-sidenav-content/div/search/page-layout/div/div/form/div[1]/div/filters/div/div/div[2]/query-item/div/predicate/div/div[2]/operators/div/mat-form-field/div/div[1]/div/mat-select/div/div[1]').click()
        time.sleep(1)
        self.driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/div/div/mat-option[2]').click()
        time.sleep(2.3483)

if __name__ == "__main__":
    pass    



























# FOR LIAM TO DECIDE WHAT TO DO WITH LATER. NO TOUCH. 

 # def parse(self, date_announced : str, location : str, location_in : bool):
    #     """parses the table that crunchbase generates based on specific parameters
        
    #     input

    #     options: a dict containing the options and their values
    #     """
        

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

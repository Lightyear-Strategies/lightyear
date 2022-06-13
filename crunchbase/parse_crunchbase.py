"""a module to scrape crunchbase website without using our crunchbase credits"""

import time, re
import pandas as pd
import undetected_chromedriver as uc
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


    def add_option(self, option : str, call : int):
        """
        a method to add an option to the query builder on crunchbase. MUST be run AFTER login()
        
        input
        
        option : string representing the name of the option you want to add
        """
        if call == 1:
            self.driver.find_element_by_xpath('/html/body/chrome/div/mat-sidenav-container/mat-sidenav-content/div/search/page-layout/div/div/form/div[1]/div/filters/query-item-add/div/button').click()
        else:
            self.driver.find_element_by_xpath('/html/body/chrome/div/mat-sidenav-container/mat-sidenav-content/div/search/page-layout/div/div/form/div[1]/div/filters/div/div/div/query-item/div/predicate/div/div[1]/query-item-add/div/button').click()
        time.sleep(3.03924857)
        if call == 1:
            mini_window = self.driver.find_element_by_xpath('//*[@id="mat-input-1"]')
        else:
            mini_window = self.driver.find_element_by_xpath('//*[@id="mat-input-3"]')
        #mini_window = self.driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/mat-dialog-container/query-item-drill-panel/div/dialog-layout/div/mat-dialog-content/div/div/div[1]/div/div/panel-search-input/mat-form-field/div/div[1]/div[4]/input')
        mini_window.send_keys(option)
        time.sleep(3.3482304897)
        mini_window.send_keys(Keys.ENTER)
        time.sleep(5.834265983)
            
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
        time.sleep(4.454)
        self.driver.find_element_by_xpath('/html/body/div[6]/div/div/div/mat-option[1]')
        #self.driver.find_element_by_xpath('/html/body/div[5]/div/div/div/mat-option[1]').click()
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

    def click_search_button(self):
        """
        a method to click the search button
        
        input
        
        None
        """
        self.driver.find_element_by_xpath('/html/body/chrome/div/mat-sidenav-container/mat-sidenav-content/div/search/page-layout/div/div/form/div[2]/results/div/div/div[1]/div/button').click()
        time.sleep(2.32414)

    def grab_table(self):
        """
        a method to grab the table and export as html source string
        
        input
        
        None
        """
        table = self.driver.find_element_by_class_name('body-wrapper')
        table_source = table.get_attribute('outerHTML')
        self.driver.quit()
        return table_source

    def compile_regex(self):
        """
        a method to compile the needed regex objects, abstracted for efficiency reasons
        
        input
        
        None
        """
        rm = re.compile('<grid-row.*?/grid-row>', flags=re.DOTALL)
        cm = re.compile('<grid-cell.*?/grid-cell>', flags=re.DOTALL)
        ffm = re.compile('<field-formatter.*?/field-formatter>', flags=re.DOTALL)
        im = re.compile('title=".*?"')
        return rm, cm, ffm, im

    def parse_table(self, table_html_string : str, row_matcher, cell_matcher, field_formatter_matcher, info_matcher):
        """
        a method to parse a single page of table information from the crunchbase funding round query builder site
        
        input
        
        table_html_string: a string of the outerHTML of the sheet-grid object from the crunchbase page
        
        row_matcher, cell_matcher, field_formatter_matcher, info_matcher: regex objects generated from self.compile_regex
        """
        rows = re.findall(row_matcher, table_html_string)
        cells = [re.findall(cell_matcher, row_string) for row_string in rows]
        formatters = [[re.findall(field_formatter_matcher, cell_string) for cell_string in cell_list] for cell_list in cells]
        infos_raw = [[re.findall(info_matcher, form[0]) for form in row_formats if len(form) > 0] for row_formats in formatters]
        info = []
        for raw_row_info in infos_raw:
            row_info = []
            for cell_info in raw_row_info:
                if len(cell_info) == 0:
                    row_info.append('N/A')
                    continue
                cell_string = ""
                for piece in cell_info:
                    to_extract = piece.split('"')[1] + " "
                    cell_string = cell_string + to_extract
                cell_string = cell_string.strip()
                if cell_string in '\u2013\u2014\u2015':
                    row_info.append('N/A')
                else:
                    row_info.append(cell_string)
            info.append(row_info)
        if self.debug:
            print('\n\n', info, '\n\n')
        df = pd.DataFrame(info, columns=['transaction_name', 'organization_name', 'funding_type', 'money_raised', 'announced_date', 'industry_tags', 'website_url', 'location_tags', 'total_funding_amount', 'crunchbase_rank', 'estimated_revenue', 'number_of_funding_rounds', 'funding_status', 'funding_stage', 'pre_money_valuation'])
        return df

    def click_next(self):
        """
        a method to click the next button when parsing a multi-page table on crunchbase
        
        input
        
        None
        """
        self.driver.find_element_by_xpath('/html/body/chrome/div/mat-sidenav-container/mat-sidenav-content/div/search/page-layout/div/div/form/div[2]/results/div/div/div[1]/div/results-info/h3/a[2]').click()
        

if __name__ == "__main__":
    parser = CrunchParse("sdjklf", "slkdfj")
    parser.driver.get("https://www.crunchbase.com/search/funding_rounds")
    time.sleep(10.1239)
    parser.add_option('announced date', 1)
    parser.add_anounced_date("1/24/2021")
    parser.add_option("location", 2)
    parser.add_location("United States")
    parser.click_search_button()
    source_html = parser.grab_table()
    rm, cm, ffm, im = parser.compile_regex()
    df = parser.parse_table(source_html, rm, cm, ffm, im)
    print(df)























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

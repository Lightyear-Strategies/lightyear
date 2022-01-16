from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import pickle
import time
import undetected_chromedriver.v2 as uc
import pandas as pd
from LDA import LDA_analysis

class Muckrack:
    def __init__(self, url_list=None, filename=None, sleep_time=2.5):
        if filename is not None:
            url_list = self.__find_list(filename)

        if(len(url_list)==1):
            self.url_list = [url_list]
        else:
            self.url_list = url_list

        self.df = pd.DataFrame()

        self.sleep_time = sleep_time
        self.time_total = len(url_list)*(self.sleep_time*2)
        self.time_left = self.time_total

    def __find_list(self, filename):
        #empty dataframe
        df = pd.DataFrame()
        url_list = []

        if(filename.endswith(".csv")):
            df = pd.read_csv(filename)
        elif(filename.endswith(".xlsx")):
            df = pd.read_excel(filename)

        #find column that's name Muckrack
        for i in range(len(df.columns)):
            if(df.columns[i]=="Muckrack" or df.columns[i]=="muckrack"
            or df.columns[i]=="Muckrack URL" or df.columns[i]=="muckrack url"):
                url_list = df.iloc[:,i]

        for i in range(len(url_list)):
            if(not url_list[i].endswith("/articles/")):
                url_list[i] = url_list[i] + "/articles/"
        return url_list

    def parse_HTML(self):
        driver = uc.Chrome()
        with driver:
            for url in self.url_list:
                print("Parsing: " + url)
                print("Time left: " + self.__time_left())
                driver.get(url)
                time.sleep(self.sleep_time)
                self.read_HTML(driver.page_source)
                time.sleep(self.sleep_time)

                self.time_left -= self.sleep_time*2
        driver.quit()

    def __time_left(self):
        time_left = self.time_left
        if(time_left<60):
            return str(time_left) + " seconds left"
        else:
            minutes = int(time_left/60)
            seconds = int(time_left%60)
            return str(minutes) + " minutes and " + str(seconds) + " seconds left"

    def read_HTML(self, page_source=None):
        if page_source is None:
            with open('savedHTML.txt', 'r') as f:
                page_source = f.read()


        soup = BeautifulSoup(page_source, "html.parser")
        aTags = soup.find_all("a", {"class": "times-shared facebook"})

        ####VARIABLES TO BE PULLED FROM HTML####
        articles = []
        medias = {}
        most_recent_date = None
        recent_topics = None
        coverage = []
        #########################################

        outlets = soup.find_all("div", {"class": "news-story-byline"})
        for outlet in range(len(outlets)):
            media = outlets[outlet].find_all("a")[-1].text
            if media in medias:
                medias[media] += 1
            else:
                medias[media] = 1

        for article in range(0, len(aTags), 2):
            articles.append(aTags[article].get("data-description"))

        most_recent_date = soup.find_all("a", {"class": "timeago"})[0].text
        recent_topics = LDA_analysis(articles, 5, 3)

        beats = soup.find_all("div", {"class": "person-details-item person-details-beats"})
        for beat in beats:
            hrefs = beat.find_all("a")
            for href in hrefs:
                coverage.append(href.text)


        #############PREPARING DATA FOR DF############
        if(len(coverage)==0):
            coverage = ["Unknown Coverage"]
        #select 3 most occuring media outlets from media
        medias = sorted(medias.items(), key=lambda x: x[1], reverse=True)
        if (len(medias) > 3):
            medias = medias[:3]
        ###############################################

        self.df = self.df.append({'Most Recent Article': most_recent_date,
                                  'Key words in last articles': recent_topics,
                                  'Focus': coverage,
                                  'Outlets': medias}, ignore_index=True)

    def save_to_csv(self, filename):
        if(len(self.df)==0):
            raise Exception("No data to convert to dataframe")
        self.df.to_csv(filename)

    def show_df(self):
        if(len(self.df)==0):
            raise Exception("No data to convert to dataframe")
        return self.df



if __name__ == '__main__':
    list_of_urls = ['https://muckrack.com/steven-melendez/articles',
                    'https://muckrack.com/joshpeter11/articles',
                    'https://muckrack.com/josh-laskin/articles']

    muck = Muckrack(list_of_urls)
    muck.parse_HTML()
    df = muck.show_df()
    print(df)


from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import pickle
import time
import undetected_chromedriver as uc

import traceback
import pandas as pd
from datetime import datetime
from datetime import timedelta

import sys
import logging
from logging import StreamHandler, Formatter

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = StreamHandler(stream=sys.stdout)
handler.setFormatter(Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))
logger.addHandler(handler)


class Muckrack:
    def __init__(self, url_journalist_list=None, filename=None, sleep_time=2.5, timeframe=7):
        if filename is not None:
            url_list = self.__find_list(filename)

        if(len(url_journalist_list)==1):
            self.url_journalist_list = [url_journalist_list]
        else:
            self.url_journalist_list = url_journalist_list

        self.df = pd.DataFrame()

        self.timeframe = timeframe
        self.sleep_time = sleep_time
        self.time_total = len(url_journalist_list)*(self.sleep_time*2)
        self.time_left = self.time_total+(self.sleep_time*2)

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
        options = uc.ChromeOptions()
        options.arguments.extend(["--no-sandbox", "--disable-setuid-sandbox", "--headless"])
        driver = uc.Chrome(options=options, driver_executable_path='/home/ubuntu/.local/bin/chromedriver',
                           browser_executable_path='/usr/bin/google-chrome')

        with driver:
            for url, journalist in self.url_journalist_list:
                self.time_left -= self.sleep_time*2
                if(type(url) is not str):
                    continue
                if(url=="" or url==" " or url=="\n" or url=="\t"):
                    continue
                if(not url.endswith("/articles")):
                    continue
                if("media-outlet" in url):
                    continue

                try:
                    logger.info("Parsing: " + url)
                    logger.info("Time left: " + self.__time_left())
                    # print("Parsing: " + url)
                    # print("Time left: " + self.__time_left())
                    driver.get(url)
                    time.sleep(self.sleep_time)
                    self.read_HTML(driver.page_source, journalist)
                    time.sleep(self.sleep_time)
                except Exception as e:
                    logger.info("Error: " + str(e))
                    traceback.print_exc(file=sys.stdout)

                    # print("Error: " + str(e))
                    continue

        driver.quit()

    def __time_left(self):
        time_left = self.time_left
        if(time_left<60):
            return str(time_left) + " seconds left"
        else:
            minutes = int(time_left/60)
            seconds = int(time_left%60)
            return str(minutes) + " minutes and " + str(seconds) + " seconds left"

    def read_HTML(self, page_source=None, journalist=None):
        if page_source is None:
            logger.info("EMPTY PAGE SOURCE")
            with open('savedHTML.txt', 'r') as f:
                page_source = f.read()


        soup = BeautifulSoup(page_source, "html.parser")
        name = soup.find_all("div", {"class": "mr-byline"})
        try:
            name_chosen = name[0].text.strip()[3:]
            position = 0
            while("," in name_chosen):
                name_chosen = name[position].text.strip()[3:]
                position += 1
                if(position>10):
                    name_chosen = name[position].split(",")[0]
        except:
            #print("Empty page")
            logger.info("Empty page")
            return
        aTags = soup.find_all("a", {"class": "times-shared facebook"})

        ####VARIABLES TO BE PULLED FROM HTML####
        articles = []
        medias = []
        coverage = []
        time_stamps = []
        headlines = []
        links = []
        journalists = []
        #########################################

        outlets = soup.find_all("div", {"class": "news-story-byline"})
        for outlet in range(len(outlets)):
            media = outlets[outlet].find_all("a")[-1].text
            medias.append(media)

        for article in range(0, len(aTags)):
            articles.append(aTags[article].get("data-description"))

        header_tags = soup.find_all("h4", {"class": "news-story-title"})
        for header in range(0, len(header_tags)):
            headlines.append(header_tags[header].text)

        time_tags = soup.find_all("a", {"class": "timeago"})
        for time in range(len(time_tags)):
            try:
                object = time_tags[time].get("title").strip()
                object = datetime.strptime(object, "%B %d, %Y %I:%M %p")
                time_stamps.append(object)
            except Exception as e:
                logger.info('\nError: ' + str(e))
                traceback.print_exc(file=sys.stdout)


        link_tags = soup.find_all("h4", {"class": "news-story-title"})
        for link in range(len(link_tags)):
             links.append(link_tags[link].find_all("a")[0].get("href"))

        #get data-description from <a class=facebook js-share-button>
        coverage_tags = soup.find_all("a", {"class": "facebook js-share-button"})
        for coverage_tag in range(len(coverage_tags)):
            coverage.append(coverage_tags[coverage_tag].get("data-description"))





        ###### ASSEMBLING DATA INTO DATAFRAME ######
        df = pd.DataFrame({})
        final_headers = []
        final_time = []
        final_media = []
        final_links = []
        final_coverage = []
        for time in range(len(time_stamps)):
            #if time is within the last 7 days
            if time_stamps[time] > datetime.now() - timedelta(days=self.timeframe):
                final_headers.append(headlines[time].replace("\n", "").replace("\t", ""))
                final_time.append(time_stamps[time].strftime("%Y-%m-%d"))
                final_media.append(medias[time])
                final_links.append(links[time])
                final_coverage.append(coverage[time])
                journalists.append(journalist)
            else:
                break

        final_names = [name_chosen]*len(final_headers)
        df = df.append(pd.DataFrame({"Name": final_names,
                                     "Headline": final_headers,
                                     "Date": final_time,
                                     "Media": final_media,
                                     "Link": final_links,
                                     "Coverage": final_coverage,
                                     "Journalist": journalists}))

        #if df is empty
        if(len(df)==0):
            logger.info("Empty Dataframe")
        else:
            self.df = self.df.append(df)
            logger.info(self.df)


    def save_dataframe(self, filename):
        if(len(self.df)==0):
            raise Exception("No data to convert to dataframe")
        self.df.to_csv(filename)

    def get_dataframe(self):
        if(len(self.df)==0):
            raise Exception("No data to convert to dataframe")
        return self.df



if __name__ == '__main__':
    list_of_urls = ['https://muckrack.com/steven-melendez/articles',
                    'https://muckrack.com/joshpeter11/articles',
                    'https://muckrack.com/josh-laskin/articles']

    muck = Muckrack(list_of_urls)
    muck.parse_HTML()
    #muck.read_HTML()

    df = muck.get_dataframe()



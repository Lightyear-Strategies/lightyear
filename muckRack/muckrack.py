from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import pickle
import time
import undetected_chromedriver.v2 as uc
import pandas as pd

class Muckrack:
    def __init__(self, url_list):
        self.url_list = []
        self.df = pd.DataFrame()

    def parse_HTML(self):
        driver = uc.Chrome()
        with driver:
            for url in self.url_list:
                driver.get(url)
                time.sleep(2)
                self.read_HTML(driver.page_source)
                time.sleep(2)
        driver.quit()


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
        self.analysis(articles)

    def analysis(self, articles):


        print(articles)




    def getArticles(self):
        return self.articles

    def getMedia(self):
        return self.media



if __name__ == '__main__':
    muck = Muckrack("https://muckrack.com/joseph-masha/articles")
    muck.read_HTML()

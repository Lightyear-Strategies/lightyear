from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import time

class Muckrack:
    def __init__(self, url):
        self.url = url
        self.soup = None

    def getHTML(self):
        driver = webdriver.Firefox()
        driver.get(self.url)
        time.sleep(15)
        self.html = driver.page_source
        driver.quit()
        with open("savedHTML.txt", "w") as f:
            f.write(self.html)

    def readHTML(self, name):
        with open(name, "r") as f:
            self.html = f.read()
        self.soup = BeautifulSoup(self.html, "html.parser")
        aTags = self.soup.find_all("a", {"class": "times-shared facebook"})
        self.articles = []
        self.media = []

        outlets = self.soup.find_all("div", {"class": "news-story-byline"})
        for media in range(len(outlets)):
            self.media.append(outlets[media].find_all("a")[-1].text)

        for article in range(0, len(aTags), 2):
            self.articles.append(aTags[article].get("data-description"))

        self.media = set(self.media)

    def getArticles(self):
        return self.articles

    def getMedia(self):
        return self.media







if __name__ == '__main__':
    test = Muckrack("https://muckrack.com/joseph-masha/articles")
    test.readHTML("savedHTML.txt")
    print(test.getMedia())

# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from goose import Goose
import re, sys, os
import urllib2, nltk

reload(sys)
sys.setdefaultencoding('utf8')

class Scrapper:
    baseUrl = "https://www.drupal.org/planet?page="

    @classmethod
    def getNodeLinks(self):
        """
        Collect 100 article links from Drupal planet aggregator.
        Note: links are from different sources
        """
        node_links = [];
        for i in range(0, 100):
            urlRequest = urllib2.Request(self.baseUrl + str(i));
            document = urllib2.urlopen(urlRequest);
            soup = BeautifulSoup(document, 'html.parser', from_encoding="utf-8");
            for link in soup.select('h3.feed-item-title a'):
                node_links.append(link.attrs['href']);
        return node_links

    @classmethod
    def getContent(self):
        g = Goose({'browser_user_agent': 'Mozilla', 'parser_class':'soup'});
        urls = self.getNodeLinks();
        for i, url in enumerate(urls):
            article = g.extract(url=url);
            self.writteFile(i, 'title', article.title);
            self.writteFile(i, 'article', article.cleaned_text);

    @classmethod
    def writteFile(self, index, type, content):
        if not os.path.exists('data'):
            os.makedirs('data')
        file = open('data/' + type + '-' + str(index) + '.txt', "w+");
        file.write(content);
        file.close();

    """Downloads the articles content."""
    def main(self):
        self.getContent();

if __name__ == '__main__':
    scrapper = Scrapper();
    scrapper.main();

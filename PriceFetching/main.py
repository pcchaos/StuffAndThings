import numpy as np
import scrapy
from scrapy.spiders import XMLFeedSpider
from scrapy.http.request import Request
from scrapy.crawler import CrawlerProcess
import datetime
from scrapy_splash import SplashRequest



__author__ = "Fynn Dierksen"
__email__ = "mail@fynn-dierksen.de"
__created__ = "06.05.2020"
__updated__ = "06.05.2020"

# TODO: Build Product class
# TODO: Build Spider / crawler
#           - For real
#           - For bringmeister / Edeka
# TODO: Enable save to file

"""
class MySpider(XMLFeedSpider):
    def __init__(self):
        self.name = 'RealPriceCrawler'

        # Domains, auf die zugegriffen werden darf
        self.allowed_daomains = ['real.de']

        self.start_urls = ['https://shop.rewe.de/p/oatly-haferdrink-barista-edition-1l/7223891']

    def start_requests(self):
        yield sp.Request(self.start_urls, self.parse_nodes())

    def parse_nodes(self, response, nodes):
"""


class DinoSpider(scrapy.Spider):
    name = "test"
    allowed_domains = ["dino.de"]
    start_urls = (
        'http://dinotools.de/blog.html',
    )

    def parse(self, response):
        s = scrapy.Selector(response)
        """
        blog_index_pages = s.xpath("//ul[@class='pagination']/li/a/@href").extract()
        print("blog_index_pages: ".format(blog_index_pages))
        print("Done")
        if blog_index_pages:
            for page in blog_index_pages:
                yield Request(response.urljoin(page), self.parse)
                
        """

        posts = s.xpath("//article")
        items = []
        for post in posts:
            print(post.xpath("header[@class='entry-header']/h2/a/text()").extract())
            print(post.xpath("header[@class='entry-header']/h2/a/@href").extract())
            print(post.xpath("div[@class='content']/p/text()").extract())

        for item in items:
            yield item


class RealSpider(scrapy.Spider):
    name = "test"
    allowed_domains = ["real.de"]
    start_urls = (
        'https://www.real.de/lebensmittelshop/Katalog/Frische/Milchersatzprodukte/Oatly-Bio-Haferdrink-Kakao/p/707984_1_1',
    )

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url=url, callback=self.parse, endpoint='render.html')

    def parse(self, response):
        s = scrapy.Selector(response)
        """
        blog_index_pages = s.xpath("//ul[@class='pagination']/li/a/@href").extract()
        print("blog_index_pages: ".format(blog_index_pages))
        print("Done")
        if blog_index_pages:
            for page in blog_index_pages:
                yield Request(response.urljoin(page), self.parse)

        """

        posts = s.xpath("food-product-price")
        items = []
        for post in posts:
            print(post.xpath("span[@class='price mr-sm']/text()").extract())
            print(post.xpath("span[@class='price mr-sm']/@data-cents").extract())

        for item in items:
            yield item


class Product():
    def __init__(self, name, price, store):
        self._name = name
        self._price = price
        self._store = store
        # Receive time, when object is created
        self._time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def __str__(self):
        return "Product {} found at {} with price {}, Timestamp: {}".format(self._name, self._store, self._price, self._time)

    def getData(self):
        return self._name, self._price, self._store, self._time

if __name__ == "__main__":
    process = CrawlerProcess({'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'})

    process.crawl(RealSpider)
    process.start()
# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request


class WenkuSpider(scrapy.Spider):
    name = 'wenku'
    allowed_domains = ['wenku.baidu.com']
    start_urls = ['http://wenku.baidu.com/']

    def start_requests(self):
        keywords = ['国网', '国家电网']
        for keyword in keywords:
            url = "https://wenku.baidu.com/search?word={}".format(keyword)
            yield Request(url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        print("=="*30)
        a = response.xpath("//a[contains(@href, 'https://wenku.baidu.com/view')]/@title").extract()
        print(a)
        pass

# -*- coding: utf-8 -*-
import scrapy


class MetasearchSpider(scrapy.Spider):
    name = 'MetaSearch'
    allowed_domains = ['MetaSearch.com']
    start_urls = ['http://MetaSearch.com/']

    def parse(self, response):
        pass

# -*- coding: utf-8 -*-
import scrapy


class PansouSpider(scrapy.Spider):
    name = 'panSou'
    allowed_domains = ['pansou.com']
    start_urls = ['http://pansou.com/']

    def parse(self, response):
        pass

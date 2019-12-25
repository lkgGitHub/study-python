# -*- coding: utf-8 -*-
import scrapy


class DocinSpider(scrapy.Spider):
    """
    豆丁：https://www.docin.com/
    """
    name = 'docin'
    allowed_domains = ['docin.com']
    start_urls = ['http://docin.com/']

    def parse(self, response):
        pass

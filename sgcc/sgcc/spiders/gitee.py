# -*- coding: utf-8 -*-
import scrapy


class GiteeSpider(scrapy.Spider):
    """
    码云：https://gitee.com/
    """
    name = 'gitee'
    allowed_domains = ['gitee.com']
    start_urls = ['http://gitee.com/']

    def parse(self, response):
        pass

# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request

ershoufang_url = "https://tj.lianjia.com/ershoufang/"


class LianjiaSpider(scrapy.Spider):
    name = 'lianjia'
    allowed_domains = ['lianjia.com']
    start_urls = ['https://tj.lianjia.com/ershoufang/']

    def parse(self, response):
        a = response.xpath("//a[contains(@href, 'https://tj.lianjia.com/ershoufang/')]/@href").extract()
        for url in a:
            print(url)
            yield Request(url=url, callback=self.parse_item)

    def parse_item(self, response):
        li = response.xpath("//div[@class='base']/div[@class='content']/ul/li")
        for l in li:
            l.response.xpath("/span")
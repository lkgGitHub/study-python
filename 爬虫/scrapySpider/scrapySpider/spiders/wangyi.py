# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy import Request

from ..items import NewsItem


class WangYiSpider(scrapy.Spider):
    name = 'wangyi'
    allowed_domains = ['money.163.com']
    start_urls = ['http://money.163.com/',
                  'https://money.163.com/special/00259BVP/news_flow_stock.js?callback=data_callback',
                  ]
    count = 0

    def start_requests(self):
        yield Request("http://money.163.com/", callback=self.parse, dont_filter=True)
        yield Request("https://money.163.com/special/00259BVP/news_flow_stock.js?callback=data_callback",
                      callback=self.parse_special, dont_filter=True)
        for i in range(2, 3):
            url = "https://money.163.com/special/00259BVP/news_flow_stock_0{}.js?callback=data_callback".format(i)
            yield Request(url, callback=self.parse_special, dont_filter=True)

    def parse(self, response):
        a = response.xpath("//a[contains(@href, 'https://money.163.com/')]/@href").extract()
        for url in a:
            yield Request(url, callback=self.parse_item)

    def parse_special(self, response):
        t = response.text[14: -1]  # 删除data_callback()
        data = json.loads(t)
        for d in data:
            url = d.get("docurl")
            yield Request(url, callback=self.parse_item)

    def parse_item(self, response):
        self.count += 1
        print("wangyi:", "=" * 20, self.count, "=" * 20)
        news = NewsItem()
        news["source"] = "wangyi"
        news["url"] = response.url
        news["title"] = response.xpath("//div[@class='post_content_main']/h1/text()").extract_first()
        news["title"] = response.xpath("/html/head/meta[@property='og:title']/@content").extract_first()
        news["summary"] = response.xpath("/html/head/meta[@name='description']/@content").extract_first()
        news["keywords"] = response.xpath("/html/head/meta[@name='keywords']/@content").extract_first()
        news["remark"] = response.xpath(
            "//div[@class='ep-source cDGray']/span[@class='left']/text()").extract_first().strip().replace("本文", "")
        news["public_time"] = response.xpath(
            "/html/head/meta[@property='article:published_time']/@content").extract_first().replace("T", " ").replace(
            "+08:00", "")

        author = response.xpath("//div[@class='ep-source cDGray']/span[@class='ep-editor']/text()").extract_first()
        start = author.find("：")
        end = author.find("_")
        if start == -1:
            start = 0
        news["author"] = author[start + 1: end]

        contents = response.xpath("//div[@id='endText']//p").xpath(
            'string(.)').extract()  # .xpath('string(.)'):解决多层嵌套的提取
        content = ""
        for c in contents:
            if "window.__STOCK_COMPONENT__.push(" not in c and "#endText ." not in c:
                content += c.replace(" ", "").replace('\n', '').replace('\r', '')
        news["content"] = content
        yield news

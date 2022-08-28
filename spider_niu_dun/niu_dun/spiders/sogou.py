# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request

base_headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,"
              "application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Host": "www.sogou.com",
    "Referer": "https://www.sogou.com/",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/79.0.3945.79 Safari/537.36 "
}

class SogouSpider(scrapy.Spider):
    """
    搜狗搜索：https://www.sogou.com/
    """
    name = 'sogou'
    allowed_domains = ['sogou.com']

    def start_requests(self):
        keyword = '牛顿'
        search_url = "https://www.sogou.com/web?query={wd}&_asf=www.sogou.com&ie=utf8&from=index-nologin&s_from=index"
        yield Request(search_url.format(wd=keyword), headers=base_headers, callback=self.parse)

    def parse(self, response):
        print(response)
        print()
        pass

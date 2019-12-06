# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request


headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Host': 'www.baidu.com',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'Referer': 'http://www.baidu.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/78.0.3904.108 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}


class BaiduSpider(scrapy.Spider):
    name = 'baidu'
    allowed_domains = ['baidu.com']
    start_urls = ['http://baidu.com/']

    def start_requests(self):
        keyword = '国网'
        url = "https://www.baidu.com/s?ie=utf-8&wd={}".format(keyword)
        yield Request(url, headers=headers, callback=self.parse)

    def parse(self, response):
        print(response.text)


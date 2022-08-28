# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request


base_headers = {
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-Mode": "navigate",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Host": "www.baidu.com",
    "is_referer": "https://www.baidu.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/78.0.3904.108 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,"
              "application/signed-exchange;v=b3",
}


class BaiduSpider(scrapy.Spider):
    name = 'baidu'
    allowed_domains = ['baidu.com']
    start_urls = ['http://baidu.com/']

    def start_requests(self):
        keyword = '牛顿'
        url = "https://www.baidu.com/s?ie=utf-8&wd={}".format(keyword)
        search_url = "https://www.baidu.com/s?ie=utf-8&wd={wd}"
        yield Request(search_url.format(wd=keyword), headers=base_headers, callback=self.parse)

    def parse(self, response):
        div = response.xpath("//div[@id='content_left']/div[@class='result c-container ']")
        print("len:", len(div))
        for d in div:
            title = d.xpath("./h3/a/text()").extract_first()
            href = d.xpath("./h3/a/@href").extract_first()
            print(title)
            print(href)

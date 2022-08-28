# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader

from ..items import PanSouItem

base_headers = {
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Host": "www.kengso.com",
    "Referer": "http://www.kengso.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/79.0.3945.79 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,"
              "application/signed-exchange;v=b3;q=0.9",
}


class PansouSpider(scrapy.Spider):
    name = 'panSou'
    allowed_domains = ['pansou.com']
    base_url = 'http://www.kengso.com/'

    def start_requests(self):
        wd = "牛顿"
        search_url = "http://www.kengso.com/s?st=0&wd={wd}".format(wd=wd)
        yield scrapy.Request(search_url, headers=base_headers)

    def parse(self, response):
        li_tags = response.xpath("//div[@class='user-share-list tubiaotype']/ul/li")
        for li in li_tags:
            href = li.xpath("./a/@href").extract_first()
            title = li.xpath("./a/@title").extract_first()
            time = li.xpath("./a/span[@class='l-size']/text()").extract_first()

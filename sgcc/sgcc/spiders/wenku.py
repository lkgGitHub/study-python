# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request

base_headers = {
    "Host": "wenku.baidu.com",
    "Referer": "https://wenku.baidu.com/",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Mode": "navigate",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/78.0.3904.108 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,"
              "application/signed-exchange;v=b3;q=0.9",
}


class WenkuSpider(scrapy.Spider):
    name = 'wenku'
    allowed_domains = ['wenku.baidu.com']
    start_urls = ['http://wenku.baidu.com/']
    search_url = 'https://wenku.baidu.com/search?word={word}org=0&fd=0&lm=0&od=0&pn={pn}'

    def start_requests(self):
        keywords = ['国家电网']
        for keyword in keywords:
            url = self.search_url.format(word=keyword, pn=10)
            print(url)
            yield Request(url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        dls = response.xpath("//div[@class='search-result']/dl")
        for dl in dls:
            title = dl.xpath("./dt[@class='logFirstClickTime mb6 clearfix']/p[@class='fl']/a/@title").extract_first()
            tag = ''.join(dl.xpath("./dd[@class='tag-tips']/a[@class='log-xsend']//text()").extract())
            summary = ''.join(dl.xpath("./dd[@class='clearfix']/div[@class='summary-box fl']/p[@class='summary lh21']//text()").extract())
            detail_info = ''.join(dl.xpath("./dd[@class='clearfix']/div[@class='summary-box fl']//div[@class='detail-info']//text()[not]").extract())
            detail_info = detail_info.replace('\n', '')
            print(title)
            print(tag)
            print(summary)
            print(detail_info)
            print("==" * 30)


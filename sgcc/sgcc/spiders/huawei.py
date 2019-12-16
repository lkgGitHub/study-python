# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,"
              "application/signed-exchange;v=b3",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Host": "appstore.huawei.com",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/78.0.3904.108 Safari/537.36"
}


class HuaweiSpider(scrapy.Spider):
    """
    华为应用商城：https://appstore.huawei.com/
    """
    name = 'huawei'
    allowed_domains = ['huawei.com']

    def start_requests(self):
        keyword = '国网'
        search_url = 'https://appstore.huawei.com/search/{}'
        yield Request(search_url.format(keyword), headers=headers)

    def parse(self, response):
        href = response.xpath("//div[@class='game-info  whole']/h4[@class='title']/a/@href").extract()
        for h in href:
            yield response.follow(h, headers=headers, callback=self.parseApp)

    def parseApp(self, response):
        title = response.xpath("//span[@class='title']/text()").extract_first()
        introduce = response.xpath("//div[@class='content']/div[@id='app_strdesc']/text()").extract_first()
        li_tags = response.xpath("//li[@class='ul-li-detail']")
        for li in li_tags:
            key = li.xpath('./text()').extract_first()
            value = li.xpath('./span/text()').extract_first()
            if '大小' in key:
                print("大小, value:{}".format(value))
            elif '日期' in key:
                print("日期, value:{}".format(value))
            elif '开发者' in key:
                print("开发者, value:{}".format(value))
            elif '版本' in key:
                print("版本, value:{}".format(value))

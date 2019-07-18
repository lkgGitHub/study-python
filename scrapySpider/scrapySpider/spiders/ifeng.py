# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy import Request

from ..items import NewsItem


class IfengSpider(scrapy.Spider):
    name = 'ifeng'
    allowed_domains = ['finance.ifeng.com']
    # start_urls = ['https://finance.ifeng.com/']
    start_urls = ['https://finance.ifeng.com/c/7oPOP0ZtxFw']

    def parse(self, response):
        news = NewsItem()
        news["url"] = response.url
        news["source"] = "ifeng"
        print("=="*30)
        script = response.xpath("/html/head/script/text()").extract()
        for s in script:
            if 'var allData' in s:
                start = s.find("var allData")
                end = s.index("};")
                print("start:{}; end:{}".format(start, end))
                data = s[start+14: end+1]
                j = json.loads(data)
                doc = j.get("docData")
                news["title"] = doc.get("title")
                news["public_time"] = doc.get("newsTime")
                news["summary"] = doc.get("summary")
                news["author"] = doc.get("editorName")
                content = ""
                content_list = doc.get("contentData").get("contentList")
                for c in content_list:
                    content += c.get("data")
                print("title:", news["title"])
                print("content:", content)
        print("==" * 30)

        content = scrapy.Field()  # 内容
        keywords = scrapy.Field()  # 关键字
        remark = scrapy.Field()  # 备注


        # a = response.xpath("//a[contains(@href, 'https://finance.ifeng.com/c')]/@href").extract()
        # print(len(a))
        # for url in a:
        #     if "#_wth_cs" in url:
        #         pass
        #     elif "special" in url:
        #         yield Request(url=url, callback=self.parse)
        #     else:
        #         yield Request(url=url, callback=self.parse_item)

    # @staticmethod
    # def parse_item(response):
    #     script = response.xpath("/html/head//script/text()").extract()
    #     if "var allData =" in script:
    #         print(script)


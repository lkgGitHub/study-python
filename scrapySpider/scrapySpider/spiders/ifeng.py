# -*- coding: utf-8 -*-
import json
import re

import scrapy
from bs4 import BeautifulSoup
from scrapy import Request

from ..items import NewsItem


class IfengSpider(scrapy.Spider):
    name = 'ifeng'
    allowed_domains = ['finance.ifeng.com']
    start_urls = ['https://finance.ifeng.com/']
    # start_urls = ['https://finance.ifeng.com/c/special/7oPi2y5Dzbk']
    count = 0

    # def start_requests(self):
    #     yield Request("https://finance.ifeng.com/c/7oM5VullK40", callback=self.parse_item)

    def parse(self, response):
        a = response.xpath("//a[contains(@href, 'https://finance.ifeng.com/c')]/@href").extract()
        print("==" * 15, len(a))
        for url in a:
            if "#_wth_cs" in url:
                pass
            elif "special" in url:
                print("special:", url)
                yield Request(url=url, callback=self.parse_special)
            else:
                yield Request(url=url, callback=self.parse_item)

    def parse_special(self, response):
        script = response.xpath("/html/head/script/text()").extract()
        for s in script:
            a = re.findall(r'"url":"https://finance.ifeng.com/(.+?)"', s)
            for u in a:
                url = 'https://finance.ifeng.com/%s' % u
                yield Request(url=url, callback=self.parse_item)

    def parse_item(self, response):
        self.count += 1
        print("ifeng:", "=" * 20, self.count, "=" * 20)
        news = NewsItem()
        news["url"] = response.url
        news["source"] = "ifeng"
        script = response.xpath("/html/head/script/text()").extract()
        for s in script:
            if 'var allData' in s:
                start = s.find("var allData")
                end = s.index("};")
                # print("start:{}; end:{}".format(start, end))
                data = s[start + 14: end + 1]
                j = json.loads(data)
                doc = j.get("docData")
                news["title"] = doc.get("title")
                news["public_time"] = doc.get("newsTime")
                news["summary"] = doc.get("summary")
                news["author"] = doc.get("editorName")
                news["remark"] = "来源:{}; 源地址: ".format(doc.get("source"), doc.get("sourceUrl"))
                content = ""
                content_list = doc.get("contentData").get("contentList")
                for c in content_list:
                    if "text" == c.get("type"):
                        soup = BeautifulSoup(c.get("data"), 'lxml')
                        for p in soup.findAll('p'):
                            content += p.text
                print("url:", response.url)
                print("title:", news["title"])
                # print("content:", content)
                news["content"] = content
        yield news

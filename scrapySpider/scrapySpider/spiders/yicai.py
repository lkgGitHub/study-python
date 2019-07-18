# -*- coding: utf-8 -*-
import json
import random
import time

import scrapy

from scrapy import Request

from ..items import NewsItem

"""
爬虫
第一财经：https://www.yicai.com/ 
"""
base_url = "https://www.yicai.com"
headers = {
    "method": "GET",
    "scheme": "https",
    "referer": "https://www.yicai.com/",
    "authority": "www.yicai.com",
    "upgrade-insecure-requests": "1",
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9",
    "x-requested-with": "XMLHttpRequest",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/75.0.3770.100 Safari/537.36 "
}


class YicaiSpider(scrapy.Spider):
    name = 'yicai'
    allowed_domains = ['yicai.com']
    count = 0

    def start_requests(self):
        total_page = 1
        page_size = 25
        for page in range(1, total_page + 1):
            yield Request(url="https://www.yicai.com/api/ajax/getlatest?page={}&pagesize={}".format(page, page_size),
                          headers=headers, dont_filter=True)  # dont_filter=True 为不过滤url

    def parse(self, response):
        headers["cache-control"] = "cache-control"
        headers["accept"] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,' \
                            'application/signed-exchange;v=b3 '
        news_list = json.loads(response.text)
        for news in news_list:
            url = news.get("url")
            if "news" in url:
                news_url = base_url + url
                print(news_url)
                yield Request(url=news_url, headers=headers, callback=self.parse_item,
                              meta={
                                  "NewsTitle": news.get("NewsTitle"),
                                  "author": news.get("NewsAuthor") + " " + news.get("CreaterName"),
                                  "pubDate": news.get("pubDate"),
                                  "NewsNotes": news.get("NewsNotes"),
                                  "remark": "频道:{}; 来源:{};".format(news.get("ChannelName"), news.get("NewsSource"))
                              })  # meta={}：请求之间传递参数，即在Request 之间传递参数
            elif "video" in url:
                print(url)
            else:
                print(url)

    def parse_item(self, response):
        self.count += 1
        print("yicai:", "=" * 20, self.count, "=" * 20)
        # time.sleep(random.uniform(1, 2))
        news_item = NewsItem()
        news_item['source'] = "yicai"
        news_item['url'] = response.url
        news_item['title'] = response.meta["NewsTitle"]
        news_item['public_time'] = response.meta["pubDate"]
        news_item['author'] = response.meta["author"]
        news_item['summary'] = response.meta["NewsNotes"]
        news_item["remark"] = response.meta["remark"]
        news_item["keywords"] = response.xpath("//meta[@name='keywords']/@content").extract_first()
        response.xpath("//div[@class_='m-txt']")
        contents = response.xpath("//div[@class='m-txt']/p/text()")
        content = ""
        for c in contents:
            content = content + c.extract()
        news_item["content"] = content
        yield news_item

    # import requests
    # from bs4 import BeautifulSoup
    # def parse_news(response):
    #     new_response = requests.get(news_url, headers=headers)
    #     news_soup = BeautifulSoup(new_response.text, 'lxml')
    #     keywords = news_soup.find("meta", attrs={"name": "keywords"})["content"]
    #     news_txt = news_soup.find("div", class_="m-txt")
    #     content = ""
    #     for p in news_txt.findAll('p'):
    #         try:
    #             content = content + p.string + "\r\n"
    #         except TypeError:
    #             pass
    #     print("keywords: %s, content: %s" % (keywords, content))
    #     news_item['content'] = content
    #     news_item["remark"] = {"频道": channel_name, "来源": news_source, "关键字": keywords}


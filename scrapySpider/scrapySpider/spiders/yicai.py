# -*- coding: utf-8 -*-
import json

import requests
import scrapy
from bs4 import BeautifulSoup
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
            news_item = NewsItem()
            channel_name = news.get("ChannelName")
            news_item['public_time'] = news.get("pubDate")
            news_item['author'] = news.get("NewsAuthor") + " " + news.get("CreaterName")
            news_source = news.get("NewsSource")
            news_item['summary'] = news.get("NewsNotes")
            news_item['title'] = news.get("NewsTitle")
            url = news.get("url")
            if "news" in url:
                news_url = base_url + url
                new_response = requests.get(news_url, headers=headers)
                news_soup = BeautifulSoup(new_response.text, 'lxml')
                keywords = news_soup.find("meta", attrs={"name": "keywords"})["content"]
                news_txt = news_soup.find("div", class_="m-txt")
                content = ""
                for p in news_txt.findAll('p'):
                    try:
                        content = content + p.string + "\r\n"
                    except TypeError:
                        pass
                print("keywords: %s, content: %s" % (keywords, content))
                news_item['content'] = content
                news_item["remark"] = {"频道": channel_name, "来源": news_source, "关键字": keywords}
            elif "video" in url:
                print(url)
            else:
                print(url)
            yield news_item

    # def parse_news(response):
    #     new_keywords = response.xpath("//meta[@name='keywords']/@content").extract_first()
    #     response.xpath("//div[@class_='m-txt']")
    #     contents = response.xpath("//div[@class='m-txt']/p/text()")
    #     content = ""
    #     for c in contents:
    #         content = content + c.extract()
    #     print("keywords:", new_keywords)
    #     print("content:", content)


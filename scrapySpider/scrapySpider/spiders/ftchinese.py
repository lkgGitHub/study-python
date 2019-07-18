# -*- coding: utf-8 -*-
import random
import time
import logging
import scrapy

from scrapy import Request
from ..items import NewsItem

base_url = "http://www.ftchinese.com"
headers = {
    'Host': 'www.ftchinese.com',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'Referer': 'http://www.ftchinese.com/',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/75.0.3770.100 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3 '
}


class FtchineseSpider(scrapy.Spider):
    name = 'ftchinese'
    allowed_domains = ['ftchinese.com']
    start_urls = [
        'http://www.ftchinese.com',  # 首页
        'http://www.ftchinese.com/channel/china.html',  # 中国
        'http://www.ftchinese.com/channel/world.html',  # 全球
        'http://www.ftchinese.com/channel/economy.html',  # 经济
        'http://www.ftchinese.com/channel/markets.html',  # 全球市场
        'http://www.ftchinese.com/channel/business.html',  # 商业
        'http://www.ftchinese.com/channel/innovation.html',  # 创新经济
        'http://www.ftchinese.com/channel/opinion.html',  # 观点
    ]

    def parse(self, response):
        for each in response.xpath('//a[contains(@href, "/story/")]/@href'):
            url = base_url + each.extract() + "?adchannelID=&full=y"
            headers['Referer'] = base_url + each.extract()
            yield Request(url, headers=headers, callback=self.parse_item)

    @staticmethod
    def parse_item(response):
        time.sleep(random.uniform(1, 2))
        title = response.xpath("//h1[contains(@class, 'story-headline')]/text()").extract_first()
        summary = response.xpath("//div[@class='story-lead']/text()").extract_first()
        authors = response.xpath("//span[@class='story-author']//text()").extract()
        contents = response.xpath("//div[@id='story-body-container']/p/text()").extract()
        remark = ""
        try:
            remark = "主题:" + response.xpath("//div[@class='story-theme']/a/text()").extract_first()
        except TypeError as e:
            logging.error(e)

        public_time = ""
        try:
            public_time = response.xpath("//span[@class='story-time']/text()").extract_first()
            public_time = public_time.replace("年", "-").replace("月", "-").replace("日", "")
        except (TypeError, AttributeError) as e:
            logging.error(e)

        content = author = ""
        for p in contents:
            content += p
        for a in authors:
            if len(a.strip()):
                author += a + " "
        if "更新于" in public_time:
            public_time = public_time[3:]
        news = NewsItem(title=title, author=author, summary=summary, content=content, public_time=public_time,
                        remark=remark, source="ftchinese", url=response.url)
        yield news

    # import re
    # from bs4 import BeautifulSoup
    # @staticmethod
    # def parse_item(response):
    #     story_soup = BeautifulSoup(response.text, "lxml")
    #     title = story_soup.find("h1", class_="story-headline").string  # <h1 class="story-headline">中美贸易摩擦：前景与应对</h1>
    #     summary = story_soup.find("div", class_="story-lead").string  # <div class="story-lead">樊磊：中美的意识形态冲突</div>
    #     remark = story_soup.find("div", class_="story-theme").find("a", href=re.compile("/tag/")).string
    #     public_time = story_soup.find("span", class_="story-time").string
    #     author = story_soup.find("span", class_="story-author").text
    #     content = ""
    #     for p in story_soup.find("div", id="story-body-container").find_all("p"):
    #         if p.string:
    #             content += p.string
    #     news = NewsItem(title=title, author=author, summary=summary, content=content, public_time=public_time,
    #                     remark=remark)
    #     yield news

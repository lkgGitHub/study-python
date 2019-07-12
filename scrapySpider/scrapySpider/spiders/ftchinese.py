# -*- coding: utf-8 -*-
import re
import scrapy
from bs4 import BeautifulSoup
from scrapy import Request

from ..items import NewsItem

base_url = "http://www.ftchinese.com"


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
            url = base_url + each.extract()
            print(url)
            yield Request(url, callback=self.parse_item)

    @staticmethod
    def parse_item(response):
        story_soup = BeautifulSoup(response.text, "lxml")
        title = story_soup.find("h1", class_="story-headline").string  # <h1 class="story-headline">中美贸易摩擦：前景与应对</h1>
        summary = story_soup.find("div", class_="story-lead").string  # <div class="story-lead">樊磊：中美的意识形态冲突</div>
        remark = story_soup.find("div", class_="story-theme").find("a", href=re.compile("/tag/")).string
        public_time = story_soup.find("span", class_="story-time").string
        author = story_soup.find("span", class_="story-author").text
        content = ""
        for p in story_soup.find("div", id="story-body-container").find_all("p"):
            if p.string:
                content += p.string
        news = NewsItem(title=title, author=author, summary=summary, content=content, public_time=public_time,
                        remark=remark)
        yield news

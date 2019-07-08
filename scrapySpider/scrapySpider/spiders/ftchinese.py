# -*- coding: utf-8 -*-
import re
import scrapy
from bs4 import BeautifulSoup


class FtchineseSpider(scrapy.Spider):
    name = 'ftchinese'
    allowed_domains = ['ftchinese.com']
    start_urls = ['http://www.ftchinese.com/']

    def parse(self, response):
        story_soup = BeautifulSoup(response.text, "lxml")
        title = story_soup.find("h1", class_="story-headline").string  # <h1 class="story-headline">中美贸易摩擦：前景与应对</h1>
        lead = story_soup.find("div", class_="story-lead")  # <div class="story-lead">樊磊：中美的意识形态冲突</div>
        tag = story_soup.find("div", class_="story-theme").find("a", href=re.compile("/tag/"))
        time = story_soup.find("span", class_="story-time").string
        print(story_soup.find("span", class_="story-author"))
        content = ""
        for p in story_soup.find("div", id="story-body-container").find_all("p"):
            if p.string:
                content += p.string + "\r\n"
        print(content)


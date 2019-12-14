# -*- coding: utf-8 -*-
import time
import logging

import scrapy
from scrapy import Request
import base64
from bs4 import BeautifulSoup

from ..items import NewsItem


class ChinaEnergySpider(scrapy.Spider):
    """
    中国能源网 [http://www.cnenergynews.cn/]
    """
    name = "ChinaEnergySpider"
    allowed_domains = ["cnenergynews.cn"]
    base_url = "http://www.cnenergynews.cn/"
    yq_url = "http://www.cnenergynews.cn/yq/"

    def start_requests(self):
        yield Request(self.yq_url)
        for page in range(1, 3):
            yield Request('http://www.cnenergynews.cn/yq/shijian_31_{}.html?t={}'.format(page, int(time.time() * 1000)))

    def parse(self, response):
        logging.info("cnenergynews(中国能源网)--parse---")
        data = response.body
        soup = BeautifulSoup(data, "lxml")
        tagsdivs = soup.find_all('div', attrs={'class': 'main4_left_m1'})
        for tags in tagsdivs:
            if tags.find('img') and (response.url == self.yq_url or response.url == self.base_url):
                continue
            title = tags.find('div', attrs={'class': 'main4_left_m1_t'}).find_all('a')[1].get_text()
            publishTime = tags.find('div', attrs={'class': 'm2'}).find('span', attrs={'class': 'b2'}).get_text()
            urlhref = tags.find('div', attrs={'class': 'main4_left_m1_t'}).find_all('a')[1].get('href')
            logging.info("title:{}, publishTime:{}".format(title, publishTime))
            yield response.follow(urlhref, meta={'title': title, 'publishTime': publishTime}, callback=self.parse_news)

    def parse_news(self, response):
        logging.info("cnenergynews(中国能源网)--parse_news---")
        title = response.meta['title']
        datetime1 = response.meta['publishTime']
        timeArray1 = time.strptime(datetime1, "%Y-%m-%d %H:%M")
        publishTime = int(time.mktime(timeArray1))
        data = response.body
        soup = BeautifulSoup(data, "lxml")
        tagsdiv = soup.find('div', attrs={'class': 'xlcontent'}).find_all('p')
        content = ''
        for tagsp in tagsdiv:
            content += tagsp.get_text().strip()
        item = NewsItem()
        item['title'] = title
        item['url'] = response.url
        item['publishTime'] = publishTime
        item['content'] = content
        item['htmlbody'] = base64.b64encode(data)
        item['siteName'] = '中国能源网'
        item['original'] = ''
        # yield item

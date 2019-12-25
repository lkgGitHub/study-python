# -*- coding: utf-8 -*-
from datetime import datetime
import time
import random
import scrapy

from ..items import AccountItem

base_headers = {
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Sec-Fetch-Mode": "navigate",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/78.0.3904.108 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,"
              "application/signed-exchange;v=b3",
}


class WechatSpider(scrapy.Spider):
    name = 'wechat'
    allowed_domains = ['weixin.sogou.com']

    # '搜公众号'url格式
    page_account_url = 'https://weixin.sogou.com/weixin?' \
                       'type=1&query={word}&_sug_type_=&s_from=input&_sug_=y&ie=utf8&page={page}'

    def start_requests(self):
        from . import get_keywords
        keyrords = get_keywords()

        account_headers = base_headers
        account_headers["Sec-Fetch-Site"] = "same-origin"
        account_headers["Referer"] = "https://weixin.sogou.com/"

        word = '国家电网'
        for page in range(1, 3):
            time.sleep(random.uniform(3, 6))
            yield scrapy.Request(url=self.page_account_url.format(word=word, page=page), headers=account_headers,
                                 dont_filter=True, callback=self.parse)

    def parse(self, response):
        """
           '搜公众号'之帐号解析
        """
        self.logger.debug(response)
        infos = response.xpath('//div[@class="news-box"]/ul[@class="news-list2"]//li')
        for info in infos:
            item = AccountItem()
            item['name'] = ''.join(info.xpath('./div//a//text()').extract())
            item['account'] = info.xpath('./div//label[@name="em_weixinhao"]/text()').extract_first()
            dls = info.xpath('./dl')
            for dl in dls:
                key = dl.xpath('./dt/text()').extract_first()
                if key == '功能介绍：':
                    item['introduction'] = ''.join(dl.xpath('./dd//text()').extract())
                elif key == '微信认证：':
                    item['authentication'] = ''.join(dl.xpath('./dd//text()').extract())
                elif key == '最近文章：':
                    item['recent_article'] = ''.join(dl.xpath('./dd/a//text()').extract())
                    timestamp = dl.xpath('./dd/span//text()').re_first('document.write\(timeConvert\(\'(.*?)\'\)\)')
                    if timestamp:
                        d_time = datetime.fromtimestamp(int(timestamp))
                        time_str = d_time.strftime("%Y-%m-%d %H:%M:%S")
                        item['update_time'] = time_str
            yield item

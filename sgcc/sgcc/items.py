# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SgccItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class PanSouItem(scrapy.Item):
    title = scrapy.Field
    url = scrapy.Field
    time = scrapy.Field()  # 时间


# 微信公众号
class AccountItem(scrapy.Item):
    name = scrapy.Field()  # 微信名
    account = scrapy.Field()  # 微信号
    introduction = scrapy.Field()  # 功能介绍
    authentication = scrapy.Field()  # 微信认证
    article_lately = scrapy.Field()  # 最近文章：
    time = scrapy.Field()  # 时间

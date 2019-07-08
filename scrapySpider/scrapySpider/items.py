# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsItem(scrapy.Item):
    title = scrapy.Field()  # 标题
    content = scrapy.Field()  # 内容
    summary = scrapy.Field()  # 摘要
    author = scrapy.Field()  # 作者
    remark = scrapy.Field()  # 备注
    public_time = scrapy.Field()  # 发布日期


class ArticleItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    weixin_name = scrapy.Field()
    time = scrapy.Field()
    content = scrapy.Field()
    url = scrapy.Field()


class AccountItem(scrapy.Item):
    name = scrapy.Field()
    account = scrapy.Field()
    recommend = scrapy.Field()
    Authentication = scrapy.Field()
    article_lately = scrapy.Field()
    time = scrapy.Field()

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
    keywords = scrapy.Field()  # 关键字
    source = scrapy.Field()  # 来源
    url = scrapy.Field()  # 原url
    author = scrapy.Field()  # 作者
    remark = scrapy.Field()  # 备注
    public_time = scrapy.Field()  # 发布日期


class ArticleItem(scrapy.Item):
    title = scrapy.Field()
    weixin_name = scrapy.Field()
    time = scrapy.Field()
    content = scrapy.Field()
    url = scrapy.Field()


class AccountItem(scrapy.Item):
    name = scrapy.Field()  # 微信名
    account = scrapy.Field()  # 微信号
    # recommend = scrapy.Field()  # 功能介绍
    # authentication = scrapy.Field()  # 微信认证
    # article_lately = scrapy.Field()  # 最近文章：
    # time = scrapy.Field()

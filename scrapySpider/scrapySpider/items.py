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

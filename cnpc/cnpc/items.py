# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    publishTime = scrapy.Field()
    content = scrapy.Field()
    htmlbody = scrapy.Field()
    original = scrapy.Field()
    siteName = scrapy.Field()

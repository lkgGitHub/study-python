# -*- coding: utf-8 -*-
import scrapy


class scrapy_spider(scrapy.Spider):
    """
    测试请求头： https://httpbin.org/get?show_env=1
    """
    name = 'scrapy_spider'
    allowed_domains = ["httpbin.org"]
    start_urls = (
        "https://httpbin.org/get?show_env=1",
    )

    # 优先级低于默认setting文件
    custom_settings = {
        "USER_AGENT": "Chrome/41.0.2228.0 Safari/537.36",
    }

    def parse(self, response):
        print(response.text)


if __name__ == '__main__':
    from scrapy import cmdline
    cmdline.execute("scrapy crawl scrapy_spider".split())

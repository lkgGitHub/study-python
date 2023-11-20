import scrapy

class HsckSpider(scrapy.Spider):
    name = 'hsck_spider'
    start_urls = ['http://686hsck.cc/vodtype/2.html']

    def parse(self, response):
        response.css()

        for title in response.css('li.stui-vodlist__box'):
            yield {'title': title.css('::text').get()}

        for next_page in response.css('a[href^="/vodtype/2"]'):
            yield response.follow(next_page, self.parse)
            
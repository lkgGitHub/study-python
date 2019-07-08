# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exporters import JsonItemExporter, CsvItemExporter


class JsonWriterPipeline(object):
    def __init__(self):
        self.file = open('news.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf-8')
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        print("==========保存到json中===========")
        self.exporter.export_item(item)
        return item


class CsvPipeline(object):

    def __init__(self):
        self.file = open('news.csv', 'wb')
        self.csv = CsvItemExporter(self.file, encoding = 'utf-8')
        self.csv.start_exporting()

    def process_item(self, item, spider):
        print("==========保存到csv中===========")
        self.csv.export_item(item)
        return item

    def close_spider(self, spider):
        self.csv.finish_exporting()
        self.file.close()

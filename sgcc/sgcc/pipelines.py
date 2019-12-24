# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql


class MySQLPipeline(object):

    # 打开数据库
    def open_spider(self, spider):
        db = spider.settings.get('MYSQL_DB_NAME', 'scrapy_db')
        host = spider.settings.get('MYSQL_HOST', 'localhost')
        port = spider.settings.get('MYSQL_PORT', 3306)
        user = spider.settings.get('MYSQL_USER', 'root')
        passwd = spider.settings.get('MYSQL_PASSWORD', '123456')
        self.db_conn = pymysql.connect(host=host, port=port, db=db, user=user, passwd=passwd, charset='utf8')
        self.db_cur = self.db_conn.cursor()

    # 关闭数据库
    def close_spider(self, spider):
        self.db_conn.commit()
        self.db_cur.close()
        self.db_conn.close()

    # 对数据进行处理
    def process_item(self, item, spider):
        if spider.name == 'wechat':
            self.insert_wechat(item)
        return item

    # 插入数据
    def insert_wechat(self, item):
        values = (
            item.get('name', ''),
            item.get('account', ''),
            item.get('introduction', ''),
            item.get('authentication', ''),
            item.get('recent_article', ''),
            item.get('update_time', None),
        )
        sql = "INSERT INTO wechat (wechat.`name`, wechat.`account`, wechat.`introduction`, wechat.`authentication`" \
              ", wechat.`recent_article`, wechat.`update_time`) VALUES (%s,%s,%s,%s,%s,%s)"
        self.db_cur.execute(sql, values)

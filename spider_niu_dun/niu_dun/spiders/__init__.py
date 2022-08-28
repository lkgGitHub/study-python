# This package will contain the spiders of your Scrapy project

import pymysql

from ..settings import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB_NAME


def get_keywords(judge=1):
    connect = pymysql.connect(host=MYSQL_HOST,
                              user=MYSQL_USER,
                              password=MYSQL_PASSWORD,
                              database=MYSQL_DB_NAME)

    # 创建游标
    cursor = connect.cursor()
    cursor.execute("select keyword from keyword WHERE judge={}".format(judge))
    # 获取剩余结果的第一行数据
    keywords = []
    data = cursor.fetchall()
    for keyword in data:
        keywords.append(keyword[0])
    cursor.close()
    connect.close()
    return keywords

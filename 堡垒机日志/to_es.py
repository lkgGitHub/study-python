import csv
import time

import xlrd
from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch import helpers

es = Elasticsearch(hosts=[{"host": "localhost", "port": 9200}])


def write_to_es():
    doc = {
        'timestamp': datetime.now(),
    }

    res = es.index(index="bastion", doc_type='log', body=doc)
    print(res['result'])

    res = es.get(index="bastion", doc_type='log', id=1)
    print(res['_source'])

    es.indices.refresh(index="bastion")

    res = es.search(index="bastion", body={"query": {"match_all": {}}})
    print("Got %d Hits:" % res['hits']['total']['value'])
    for hit in res['hits']['hits']:
        print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])


def read_xlsx():
    book = xlrd.open_workbook('日志样例.xlsx')
    sheet = book.sheet_by_index(0)
    print("行数：", sheet.nrows)
    print("列数：", sheet.ncols)
    # print(sheet.cell(0, 0).value)
    # print(sheet.row_values(0))  # 获取到整行的内容
    # print(sheet.col_values(0))  # 获取到整列的内容

    for i in range(sheet.nrows):  # 循环获取每行的内容
        print(sheet.row_values(i))


def xlsx_to_es():
    book = xlrd.open_workbook('日志样例.xlsx')
    sheet = book.sheet_by_index(0)
    header = sheet.row_values(0)
    for i in range(sheet.nrows):
        cols = sheet.row_values(i)
        doc = dict(zip(header, cols))
        doc['timestamp'] = datetime.now()
        res = es.index(index="bastion", body=doc)
        print(res['result'])


def csv_to_es(file_path):
    with open(file_path, mode='r', encoding='latin1') as f_csv:
        csv_reader = csv.DictReader(f_csv)
        while True:
            boo = False
            body = []
            for i in range(50000):
                row = next(csv_reader, False)
                if row:
                    body.append({'_index': 'bastion', '_source': dict(row)})
                else:
                    boo = True
                    break
            res = helpers.bulk(es, body, chunk_size=50000, request_timeout=200)
            print(res)
            if boo:
                break
    # 小数量文件
    # with open(file_path, mode='r', encoding='latin1') as f_csv:
    #     csv_reader = csv.DictReader(f_csv)
    #     for i in range(1000):
    #         body = [
    #             {
    #                 '_index': 'bastion',
    #                 '_source': dict(row)
    #             }
    #             for row in csv_reader
    #         ]
    #     from elasticsearch import helpers
    #     # 批量插入es中
    #     res = helpers.bulk(es, body, chunk_size=1000, request_timeout=200)
    #     print(res)


def read_csv(file_path):
    with open(file_path, mode='r', encoding='latin1') as f_csv:
        # reader = csv.reader(f_csv)
        reader = csv.DictReader(f_csv)
        # for line in reader:
        reader = reader[0:3]
        for line in reader:
            print(line)

if __name__ == '__main__':
    start = time.time()
    # path = 'D:\\01Work\\04微智日志分析\\移动堡垒机日志样本\\日志样例.csv'
    path = 'D:\\01Work\\04微智日志分析\\堡垒机日志\\北京中心业务系统近半年系统操作日志.csv'
    csv_to_es(path)
    print("用时：", int(time.time() - start), "s")

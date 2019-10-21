import csv
import os
import random
import threading
import time

from elasticsearch import Elasticsearch, ConnectionTimeout

'''
/_cat/indices
/energy_search/_search
'''

invalid_word = ['订阅', '手机短信', '短信', '免费试用', '标准', '时间', '单位', '报告', '作者', '原文', '主要', '公开',
                '申请', '会议', '进行', '类型', '公告', '通过', '摘要', '日期', '自由', '出处', '名称', '全文', '图表',
                '所有者', '译者', '地址', '团体', 'pdf', '文献', '期刊', '汇编', 'check', 'date', 'filename', 'fld',
                'sys', 'sysid',  '主办单位', '主题词', '书名', '出版者', '分类号', '副题', '发布日期', '实施日期',
                '开本', '文摘', '申请者', '索取', '译文', '页码', '题名', '研究', '分析', '影响', '关键词']
es_pool = [Elasticsearch('11.11.210.137'),
           Elasticsearch('11.11.210.138'),
           Elasticsearch('11.11.210.139'),
           Elasticsearch('11.11.210.140'),
           Elasticsearch('11.11.210.141'),
           Elasticsearch('11.11.210.142'),
           Elasticsearch('11.11.210.143'),
           Elasticsearch('11.11.210.144')]
# es = Elasticsearch('11.11.210.141')
index = 'energy_search'
start = time.time()
start_time = '2014-01-01'  # 1388505600
end_time = 1389283200  # int(time.time())
total_count = 500


def csv_writer_header(content):
    body = {
        "query": {
            "bool": {
                "must": [
                    {
                        "term": {
                            "content": content
                        }
                    }
                ]
            }
        },
        "size": 0,
        "aggs": {
            "messages": {
                "terms": {
                    "size": 1000,
                    "field": "content"
                }
            }
        }
    }
    response = {}
    count = 0
    try:
        response = es_pool[random.randint(0, 7)].search(index=index, body=body, request_timeout=10000)
    except ConnectionTimeout as e:
        print("连接超时:", int(time.time() - start), "s")
        print(response['hits'])
    header_words = ['时间']
    for bucket in response['aggregations']['messages']['buckets']:
        key = bucket['key']
        doc_count = bucket['doc_count']
        if len(key) != 1 and key not in invalid_word and not key.isdigit():
            count += 1
            header_words.append(bucket.get("key"))
        if count == total_count:
            break
    print("count:", count)
    print("高频词统计用时:", int(time.time() - start), "s")
    with open(content + '.csv', 'a+', newline='', encoding='utf_8_sig') as f:
        writer = csv.writer(f)
        writer.writerow(header_words)


# 查询一行数据
def counts(words, keyword, gte):
    row = [gte]
    for word in words:
        body = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "term": {
                                "content": keyword
                            }
                        },
                        {
                            "term": {
                                "content": word
                            }
                        }
                    ],
                    "filter": {
                        "range": {
                            "publish_time": {
                                "gte": gte,
                                "lte": gte + 86400
                            }
                        }
                    }
                }
            },
            "size": 0,
            "aggs": {
                "messages": {
                    "terms": {
                        "size": 100,
                        "field": "content"
                    }
                }
            }
        }
        es = es_pool[random.randint(0, 7)]
        response = es.search(index=index, body=body, request_timeout=10000)
        word_count = 0
        for bucket in response['aggregations']['messages']['buckets']:
            if bucket.get("key") == word:
                word_count = bucket.get("doc_count")
                break
        row.append(word_count)
    return row


def timeStamp_to_date(timeStamp):
    timeArray = time.localtime(timeStamp)
    return time.strftime("%Y-%m-%d", timeArray)


def date_to_timeStamp(format_date):
    ts = time.strptime(format_date, "%Y-%m-%d")
    return int(time.mktime(ts))


def csv_write_row(name, headers, start_timeStamp):
    with open('{}/{}{}.csv'.format(name, name, timeStamp_to_date(start_timeStamp)), 'w',
              newline='', encoding='utf_8_sig') as f:
        writer = csv.writer(f)
        row = counts(headers, name, start_timeStamp)
        writer.writerow(row)
    print(timeStamp_to_date(start_timeStamp)+"用时:", int(time.time() - start), "s")


def merge():
    name_dir = "天然气"
    rows_merge = []
    files = os.listdir(name_dir)
    file_list = []
    for file in files:  # 遍历文件夹
        if not os.path.isdir(file):
            file_list.append(name_dir + '/' + file)
    for file_path in file_list:
        with open(file_path, 'r', newline='', encoding='utf_8_sig') as merge_f:
            merge_csv = csv.reader(merge_f)
            merge_header = next(merge_csv)
            if len(merge_header) == 501:
                rows_merge.append(merge_header)
            else:
                print(file_path)
    with open('{}.csv'.format(name_dir), 'a+', newline='', encoding='utf_8_sig') as merge_f:
        writer_merge = csv.writer(merge_f)
        rows_merge = sorted(rows_merge, key=lambda x: x[0], reverse=False)
        for row_merge in rows_merge:
            time_merge = row_merge[0]
            row_merge[0] = timeStamp_to_date(int(time_merge))
            writer_merge.writerow(row_merge)


if __name__ == '__main__':
    begin = time.time()
    merge()
    # name = "液化气"
    # # csv_writer_header("液化石油气")
    # # csv_writer_header("液化气")
    # # csv_writer_header("天然气")
    # # csv_writer_header("原油")
    #
    # with open(name + '.csv', 'r', newline='', encoding='utf_8_sig') as f:
    #     f_csv = csv.reader(f)
    #     headers = next(f_csv)
    #     del(headers[0])
    #     start_date = "2016-01-02"
    #     start_time = date_to_timeStamp(start_date)
    #     tread_count = 0
    #     while start_time <= date_to_timeStamp("2019-09-16"):
    #         t = threading.Thread(target=csv_write_row, args=(name, headers, start_time,), daemon=True)
    #         t.start()
    #         start_time += 86400
    #         tread_count += 1
    #
    #     while True:
    #         length = len(threading.enumerate())  # 枚举返回个列表
    #         print('running threads：{}; 用时:{}s'.format(length, int(time.time()-begin)))
    #         time.sleep(10)
    #         if length <= 4:
    #             break

    print("总共用时：", int(time.time()-begin))



# import csv
# import time
#
# from elasticsearch import Elasticsearch, ConnectionTimeout
#
# '''
# /_cat/indices
# /energy_search/_search
# '''
#
# invalid_word = ['订阅', '手机短信', '短信', '免费试用']
# es = Elasticsearch('11.11.210.141')
# index = 'energy_search'
# content = "液化石油气"
# start = time.time()
# start_time = '2014-01-01 00:00:00'  # 1388505600
# end_time = 1389283200  # int(time.time())
# total_count = 500
#
#
# def main():
#     body = {
#         "query": {
#             "bool": {
#                 "must": [
#                     {
#                         "term": {
#                             "content": content
#                         }
#                     }
#                 ],
#                 "filter": {
#                     "range": {
#                         "publish_time": {
#                             "gte": 1388505600,
#                             "lte": 1389283200
#                         }
#                     }
#                 }
#             }
#         },
#         "size": 0,
#         "aggs": {
#             "messages": {
#                 "terms": {
#                     "size": 1000,
#                     "field": "content"
#                 }
#             }
#         }
#     }
#     response = {}
#     count = 0
#     try:
#         response = es.search(index=index, body=body, request_timeout=10000)
#     except ConnectionTimeout as e:
#         print("连接超时:", int(time.time() - start), "s")
#         print(response['hits'])
#     buckets = []
#     for bucket in response['aggregations']['messages']['buckets']:
#         key = bucket['key']
#         doc_count = bucket['doc_count']
#         if len(key) != 1 and key not in invalid_word and not key.isdigit():
#             count += 1
#             buckets.append(bucket)
#         if count == total_count:
#             break
#     print("count:", count)
#     print("高频词统计用时:", int(time.time() - start), "s")
#     return buckets
#
#
# def counts(buckets, gte):
#     row = [timeStamp_to_date(gte)]
#     for bu in buckets:
#         word = bu.get("key")
#         body = {
#             "query": {
#                 "bool": {
#                     "must": [
#                         {
#                             "term": {
#                                 "content": content
#                             }
#                         },
#                         {
#                             "term": {
#                                 "content": word
#                             }
#                         }
#                     ],
#                     "filter": {
#                         "range": {
#                             "publish_time": {
#                                 "gte": gte,
#                                 "lte": gte + 86400
#                             }
#                         }
#                     }
#                 }
#             },
#             "size": 0,
#             "aggs": {
#                 "messages": {
#                     "terms": {
#                         "size": 100,
#                         "field": "content"
#                     }
#                 }
#             }
#         }
#         response = es.search(index=index, body=body, request_timeout=10000)
#         word_count = 0
#         for bucket in response['aggregations']['messages']['buckets']:
#             if bucket.get("key") == word:
#                 word_count = bucket.get("doc_count")
#                 break
#         row.append(word_count)
#     return row
#
#
# def timeStamp_to_date(timeStamp):
#     timeArray = time.localtime(timeStamp)
#     return time.strftime("%Y-%m-%d", timeArray)
#
#
# if __name__ == '__main__':
#     buckets = main()  # {'key': '液化石油气', 'doc_count': 57057}
#     print(buckets)
#     # headers = ['时间']
#     headers = [content]
#     for b in buckets:
#         headers.append(b.get("key"))
#     print(headers)
#     # with open(content + '.csv', 'a+', newline='', encoding='utf_8_sig') as f:
#     #     writer = csv.writer(f)
#     #     writer.writerow(headers)
#
#         # ts = time.strptime(start_time, "%Y-%m-%d %H:%M:%S")
#         # gte = int(time.mktime(ts))
#         # while gte < end_time:
#         #     row_time = time.time()
#         #     row = counts(buckets, gte)
#         #     writer.writerow(row)
#         #     print(timeStamp_to_date(gte), "用时:", int(time.time() - row_time), row)
#         #     gte += 86400
#
#     print("总用时:", int(time.time() - start), "s")

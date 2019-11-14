import csv
import threading
import time

import xlrd
from datetime import datetime
from elasticsearch import Elasticsearch, TransportError
from elasticsearch import helpers

es = Elasticsearch(hosts=[{"host": "localhost", "port": 9200}])


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


def csv_to_es(base_path, n):
    head = ["CMD_ID", "SESSION_ID", "CMD", "CONTENT", "OP_TIME", "OP_DIRECTORY", "IS_EXCUTE", "AUDIT_LEVEL_ID",
            "AUDIT_LEVEL_NAME", "AUDIT_TYPE_ID", "AUDIT_TYPE_NAME", "ACTION_TYPE_ID", "ACTION_TYPE_NAME", "OBJ_TYPE_ID",
            "OBJ_TYPE_NAME", "DATA_TYPE_ID", "DATA_TYPE_NAME", "OPERATE_TYPE_ID", "OPERATE_TYPE_NAME", "SENSITIVITY",
            "CREATE_TIME", "BANK_APPROVE", "BANKFLAG", "BANK_ISNEED", "GOLD_APPR_MAIN_ACCT_ID", "GOLD_APPR_PERSON_NAME",
            "BANK_ISOPEN", "BANK_SCENE_ID", "BANK_SCENE_NAME", "BANK_APPLY_TYPE", "BANK_LAST_CHECK_STATUS",
            "BANK_LAST_CHECK_TIME", "BANK_FAIED_CHECK_COUNT", "BANK_TRIGGER_TYPE", "AUDIT_SUB_TYPE_ID",
            "AUDIT_SUB_TYPE_NAME", "OPERATE_OBJECT_TYPE", "ORI_CREATE_TIME", "STD_CREATE_TIME", "LEVEL2_ORG_ID",
            "LEVEL2_ORG_NAME", "ORI_FILE_NAME", "ORI_FILE_ROWNUM", "ORI_GATHER_TIME", "RECHECK_DATA_ID",
            "STD_BEGIN_TIME", "OBJ_TABLES", "OBJ_FILES", "DEVICE_TYPE", "PERSON_NAME", "PERSON_AREA_ID",
            "PERSON_AREA_NAME", "PERSON_ORG_ID", "PERSON_ORG_NAME", "PERSON_STATUS_ID", "PERSON_STATUS", "MAIN_ACCT_ID",
            "MAIN_ACCT_NAME", "MAIN_ACCT_STATUS_ID", "MAIN_ACCT_STATUS", "SUB_ACCT_ID", "SUB_ACCT_NAME",
            "SUB_ACCT_STATUS_ID", "SUB_ACCT_STATUS", "SUB_ACCT_TYPE_ID", "SUB_ACCT_TYPE_NAME", "CLIENT_NAME",
            "CLIENT_IP", "CLIENT_AREA_ID", "CLIENT_AREA_NAME", "CLIENT_IP_SECTION_ID", "CLIENT_IP_SECTION_NAME",
            "CLIENT_MAC", "CLIENT_CPU_SERIAL", "PROTOCOL", "DEVICE_ID", "DEVICE_IP", "DEVICE_NAME", "DEVICE_PORT",
            "SERVER_IP_SECTION_ID", "SERVER_IP_SECTION_NAME", "DEVICE_OS_VERSION", "CMD_SUMMARY", "LOGIN_TIME",
            "LOGOUT_TIME", "IS_WORK_TIME", "IS_WORK_DAY", "PERSON_DUTY_ID", "PERSON_DUTY_NAME", "TASK_NO", "LOG_SOURCE",
            "DB_INSTANCE_NAME", "OPERATE_RESULT", "CLIENT_DEVICE_PORT", "ACTION", "PASSTYPE", "DEVICE_MAINTAINER",
            "DEVICE_IMPORT_LEVEL", "DEVICE_MAINTAINER_ID", "ACCT_TYPE", "REMARK", "EFFECT_TIME", "EXPIRE_TIME",
            "ACCT_TYPE_NAME"]
    for b in range(5):
        file_path = base_path + str(n*10 + b) + ".csv"
        with open(file_path, mode='r') as f_csv:  # encoding='latin1'
            reader = csv.reader(f_csv)
            while True:
                boo = False
                body = []
                for i in range(30000):
                    try:
                        row = next(reader, False)
                    except UnicodeDecodeError as e:
                        print(next(reader, False))
                        continue
                    if row:
                        body.append({'_index': 'bastion', '_source': dict(zip(head, row))})
                    else:
                        boo = True
                        break
                for r in range(10):
                    try:
                        res = helpers.bulk(es, body, chunk_size=30000, request_timeout=5000)
                        print(res)
                        break
                    except TransportError as t:
                        print("=="*30)
                        print(file_path)
                        print("=="*30)
                if boo:
                    break


if __name__ == '__main__':
    start = time.time()
    # path = 'D:\\01Work\\04微智日志分析\\移动堡垒机日志样本\\日志样例.csv'
    # path = 'D:\\01Work\\04微智堡垒机日志\\堡垒机日志\\北京中心业务系统近半年系统操作日志.csv'
    path = 'D:\\01Work\\04微智堡垒机日志\\堡垒机日志\\log\\bastion'
    # csv_to_es(path)
    # for a in range(0, 9):
    t = threading.Thread(target=csv_to_es, args=(path, 9), daemon=True)
    t.start()

    while True:
        length = len(threading.enumerate())  # 枚举返回个列表
        print('running threads：{}; 用时:{}s'.format(length, int(time.time() - start)))
        time.sleep(10)
        if length <= 4:
            break
    print("用时：", int(time.time() - start), "s")



# def csv_to_es1(file_path):
#     # 小数量文件
#     with open(file_path, mode='r', encoding='latin1') as f_csv:
#         csv_reader = csv.DictReader(f_csv)
#         for i in range(1000):
#             body = [
#                 {
#                     '_index': 'bastion',
#                     '_source': dict(row)
#                 }
#                 for row in csv_reader
#             ]
#         from elasticsearch import helpers
#         # 批量插入es中
#         res = helpers.bulk(es, body, chunk_size=1000, request_timeout=200)
#         print(res)
#
#
# def write_to_es():
#     doc = {
#         'timestamp': datetime.now(),
#     }
#
#     res = es.index(index="bastion", doc_type='log', body=doc)
#     print(res['result'])
#
#     res = es.get(index="bastion", doc_type='log', id=1)
#     print(res['_source'])
#
#     es.indices.refresh(index="bastion")
#
#     res = es.search(index="bastion", body={"query": {"match_all": {}}})
#     print("Got %d Hits:" % res['hits']['total']['value'])
#     for hit in res['hits']['hits']:
#         print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])
#
#
# def read_xlsx():
#     book = xlrd.open_workbook('日志样例.xlsx')
#     sheet = book.sheet_by_index(0)
#     print("行数：", sheet.nrows)
#     print("列数：", sheet.ncols)
#     # print(sheet.cell(0, 0).value)
#     # print(sheet.row_values(0))  # 获取到整行的内容
#     # print(sheet.col_values(0))  # 获取到整列的内容
#
#     for i in range(sheet.nrows):  # 循环获取每行的内容
#         print(sheet.row_values(i))
#
#
# def csv_to_es(file_path):
#     with open(file_path, mode='r') as f_csv:  # encoding='latin1'
#         csv_reader = csv.DictReader(f_csv)
#         while True:
#             boo = False
#             body = []
#             for i in range(30000):
#                 row = next(csv_reader, False)
#                 print(row['PERSON_NAME'])
#                 if row:
#                     body.append({'_index': 'bastion', '_source': dict(row)})
#                 else:
#                     boo = True
#                     break
#             res = helpers.bulk(es, body, chunk_size=30000, request_timeout=200)
#             print(res)
#             if boo:
#                 break


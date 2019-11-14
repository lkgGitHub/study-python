import csv

from elasticsearch import Elasticsearch, TransportError
from elasticsearch import helpers

es = Elasticsearch(hosts=[{"host": "localhost", "port": 9200}])

def es_search():
    rows = []
    row = []
    body = {
        "query": {
            "match_all": {}
        },
        "size": 0,
        "aggs": {
            "groupby-fiel": {
                "terms": {
                    "field": "PERSON_NAME.keyword",
                    "size": 10
                },
                "aggs": {
                    "groupby-fiel": {
                        "terms": {
                            "field": "CMD.keyword",
                            "size": 10
                        }
                    }
                }
            }
        }
    }
    request = es.search(index='bastion', body=body)
    buckets = request['aggregations']["groupby-fiel"]['buckets']
    for bucket in buckets:
        key = bucket['key']
        doc_count = bucket['doc_count']
        sub_buckets = bucket['groupby-fiel']['buckets']
        for sub_bucket in sub_buckets:
            sub_key = sub_bucket['key']
            sub_doc_count = sub_bucket['doc_count']

def write_csv(headers: [], rows: []):
    with open('stocks.csv', 'w') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(headers)
        f_csv.writerows(rows)


if __name__ == '__main__':


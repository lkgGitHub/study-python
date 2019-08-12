from os import path
import csv

import jieba

if __name__ == '__main__':
    d = path.dirname(__file__)
    with open(d+"/news.csv", encoding='utf-8') as f:
        f_csv = csv.reader(f)
        headers = next(f_csv)

        text = str(f_csv)
        wordlist = jieba.cut(text, cut_all=True)
        print("Full Mode: " + "/ ".join(wordlist))  # 全模式


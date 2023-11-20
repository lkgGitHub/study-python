from os import path
import csv

import jieba
from wordcloud import WordCloud
from PIL import Image
import matplotlib
import numpy as np
import matplotlib.pyplot as plt

word_dict = {}


def wordcount(word_list: []) -> {}:
    for word in word_list:
        if word == "":
            continue
        word = word.strip()
        if word in word_dict:
            word_dict[word] += 1
        else:
            word_dict[word] = 1
    return word_dict


if __name__ == '__main__':
    d = path.dirname(__file__)
    with open(d + "/news.csv", encoding='utf-8') as f:
        f_csv = csv.reader(f)
        headers = next(f_csv)

        for row in f_csv:
            # [author,content,keywords,public_time,remark,source,summary,title,url]
            wordlist = jieba.cut(row[1], cut_all=True)
            wordcount(wordlist)
        words = sorted(word_dict.items(), key=lambda k: k[1], reverse=True)
        print(type(words))

        word_fre_dic = {x[0]: x[1] for x in words}
        # 2.设置词云的背景颜色、宽高、字数
        wordcloud = WordCloud(font_path='/System/Library/Fonts/STHeiti Light.ttc',
                              background_color="black", width=600,
                              height=300, max_words=50).fit_words(word_fre_dic)
        # 3.生成图片
        image = wordcloud.to_image()
        # 4.显示图片
        image.show()

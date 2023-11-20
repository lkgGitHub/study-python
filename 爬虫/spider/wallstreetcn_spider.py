import re

import requests
from bs4 import BeautifulSoup
"""
华尔街见闻爬虫
https://wallstreetcn.com/
"""
base_url = "https://wallstreetcn.com"
# 资讯
base_news_url = "https://wallstreetcn.com/news/global"
headers = {
    'authority': 'wallstreetcn.com',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'accept-encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/74.0.3729.169 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3 ',
}

def parse_articles(articles_url):
    articles_headers = headers
    articles_headers['referer'] = 'https://wallstreetcn.com/news/global'
    response = requests.get(articles_url, headers=articles_headers)
    soup = BeautifulSoup(response.text, "lxml")
    article = soup.find("article", class_="article")
    header = article.find("header", class_="article-header")
    title = header.find("h1", class_="title").string
    author = header.find("div", class_="meta-item author").find("span", class_="blk").string
    time = header.find("time", class_="meta-item time").string
    summary = article.find("div", class_="article-summary").string
    ps = article.find("div", class_="rich-text").find_all("p")
    content = ""
    for p in ps:
        print(p.get_text())
        content += p.get_text() + '\r\n'
    print(content)

if __name__ == '__main__':
    # response = requests.get(base_news_url, headers=headers)
    # soup = BeautifulSoup(response.text, "lxml")
    # hrefs = soup.find_all("a", class_="article-link title", href=re.compile("^/articles/"))
    # print("hrefs size:", len(hrefs))
    # for href in hrefs:
    #     parse_articles(base_url+href['href'])
    parse_articles("https://wallstreetcn.com/articles/3539824")
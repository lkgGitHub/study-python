import json
import requests
from bs4 import BeautifulSoup
"""
爬虫
第一财经：https://www.yicai.com/ 
"""
base_url = "https://www.yicai.com"
headers = {
    "authority": "www.yicai.com",
    "method": "GET",
    "scheme": "https",
    "referer": "https://www.yicai.com/",
    "upgrade-insecure-requests": "1",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,"
              "application/signed-exchange;v=b3",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/74.0.3729.169 Safari/537.36 "
}


def parse_news(new_url):
    new_response = requests.get(new_url, headers=headers)
    news_soup = BeautifulSoup(new_response.text, 'lxml')
    new_keywords = news_soup.find("meta", attrs={"name": "keywords"})["content"]
    news_txt = news_soup.find("div", class_="m-txt")
    news_content = ""
    for p in news_txt.findAll('p'):
        try:
            news_content = news_content + p.string + "\r\n"
        except TypeError:
            pass
    return new_keywords, news_content


if __name__ == '__main__':
    page_size = 30
    page = 1
    page_url = "https://www.yicai.com/api/ajax/getlatest?page={}&pagesize={}".format(page, page_size)
    response = requests.get(page_url, headers=headers)
    news_list = json.loads(response.text)
    for news in news_list:
        channel_name = news.get("ChannelName")
        create_name = news.get("CreaterName")
        news_createDate = news.get("CreateDate")
        news_pubDate = news.get("pubDate")
        news_author = news.get("NewsAuthor")
        news_source = news.get("NewsSource")
        news_title = news.get("NewsTitle")
        url = news.get("url")
        if "news" in url:
            print(base_url + url)
            # (keywords, content) = parse_news(base_url + url)
            # print("keywords: %s, content: %s" % (keywords, content))
        elif "video" in url:
            print(url)
        else:
            print(url)

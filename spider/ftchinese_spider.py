import re

import requests
from bs4 import BeautifulSoup

base_url = "http://www.ftchinese.com"
headers = {
    'Host': 'www.ftchinese.com',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'Referer': 'http://www.ftchinese.com/',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/74.0.3729.169 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3 '
}


def parse_news(story_url):
    story_response = requests.get(story_url + "?adchannelID=&full=y", headers=headers)
    story_soup = BeautifulSoup(story_response.text, "lxml")
    title = story_soup.find("h1", class_="story-headline").string  # <h1 class="story-headline">中美贸易摩擦：前景与应对</h1>
    lead = story_soup.find("div", class_="story-lead")  # <div class="story-lead">樊磊：中美的意识形态冲突</div>
    tag = story_soup.find("div", class_="story-theme").find("a", href=re.compile("/tag/"))
    time = story_soup.find("span", class_="story-time").string
    print(story_soup.find("span", class_="story-author"))
    content = ""
    for p in story_soup.find("div", id="story-body-container").find_all("p"):
        if p.string:
            content += p.string + "\r\n"
    print("title:", title)
    print(content)


if __name__ == '__main__':
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, "lxml")
    soups = soup.find_all("a",class_=re.compile("item-headline-link"), href=re.compile("/story/"))# 等价于：soups = soup.find_all("a", attrs={"class": re.compile("item-headline-link"), "href": re.compile("/story/")})
    print(len(soups))
    # for s in soups:
    #     print(s)
    parse_news(base_url + "/story/001083476")

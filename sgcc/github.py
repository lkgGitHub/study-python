# -*- coding: utf-8 -*-
import json
import requests


if __name__ == '__main__':
    search_url = 'https://api.github.com/search/repositories?q={word}&sort=best match&order=desc'
    word = '国网'
    url = search_url.format(word=word)
    resopnse = requests.get(url)
    data = json.loads(resopnse.text)
    total_count = data.get('total_count')
    items = data.get('items')
    for item in items:
        html_url = item.get('html_url')
        description = item.get('description')
        updated_at = item.get('updated_at')
        # readme = requests.get(html_url+"/blob/master/README.md")



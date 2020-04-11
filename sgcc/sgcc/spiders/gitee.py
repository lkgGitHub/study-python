# -*- coding: utf-8 -*-
import json
import requests

headers = {
    "Content-Type": "application/json",
    "charset": "UTF-8"
}

if __name__ == '__main__':
    search_url = 'https://gitee.com/api/v5/search/repositories?q={wd}page={page}&per_page=3&order=desc'
    word = '国网'
    page = 1
    url = search_url.format(word=word, page=page)
    resopnse = requests.get(url, headers=headers)
    data = json.loads(resopnse.text)
    root = data.get('root')
    items = root.get('items')
    for item in items:
        html_url = item.get('html_url')
        description = item.get('description')
        updated_at = item.get('updated_at')
        # readme = requests.get(html_url+"/blob/master/README.md")

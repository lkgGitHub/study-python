import requests

if __name__ == '__main__':
    url = "https://www.yicai.com"
    page = 2
    page_size = 10
    page_url = "https://www.yicai.com/api/ajax/getlatest?page={}&pagesize={}".format(page, page_size)
    response = requests.get(page_url)
    print(response.text)

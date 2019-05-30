import requests

if __name__ == '__main__':
    url = "http://www.ftchinese.com/"
    response = requests.get(url)
    print(response.status_code)
    print(response.text)
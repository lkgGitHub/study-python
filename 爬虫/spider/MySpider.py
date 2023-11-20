import requests
from bs4 import BeautifulSoup
import time
import re


def dowload(name, src):
    r = requests.get(src)
    with open('../data/%s.jpg' % name, 'wb') as f:
        f.write(r.content)


if __name__ == '__main__':
    start = time.time()
    base_url = "https://www.lsm.me/"
    page = 2
    lsm = "https://www.lsm.me/plugin.php?id=group&page=%s" % page
    content = requests.get(lsm, timeout=10)
    res = r'<a href="thread-.*? target="_blank"/>'
    urls = re.findall(r'<a href="thread-.*? target="_blank">', content.text, re.I | re.S | re.M)
    for u in urls:
        for i in range(1, 5):
            url = "https://www.lsm.me/thread-%s-%s-1.html" % (u[16:21], i)
            html = requests.get(url)
            if html.status_code == 200:
                soup = BeautifulSoup(html.text, 'html.parser')
                img_list = soup.find_all("img")
                for img in img_list:
                    if img.get("alt") and not img.get("border"):
                        dowload(img.get("alt")+str(i), img.get("src"))
    print("y用时：", (time.time() - start))

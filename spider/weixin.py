import csv
import random

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time

headers = {
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Referer': 'https://weixin.sogou.com/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3 ',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/75.0.3770.90 Safari/537.36'
}

url = "https://weixin.sogou.com/weixin"


if __name__ == '__main__':
    # 设置代理
    PROXY = "61.168.162.32:80"
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--proxy-server=http://124.232.133.199:3128")

    driver = webdriver.Chrome('/Users/mac/software/chromedriver', options=chrome_options)
    driver.get(url)
    time.sleep(random.uniform(0, 2))
    i = 1
    with open("filename.csv", "r") as csvfile:
        reader = csv.reader(csvfile)
        for r in reader:
            print(str(i) + ":" + str(r))
            i = i + 1
            # driver = webdriver.Chrome('C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver')
            # query_url = "https://weixin.sogou.com/weixin?type=1&query={}&ie=utf8&s_from=input&_sug_=y&_sug_type_=".format("石油")
            try:
                driver.find_element_by_id("query").clear()
                driver.find_element_by_id("query").send_keys(r[1])
            except NoSuchElementException as e:
                print("更换代理")
            time.sleep(random.uniform(1, 3))
            driver.find_element_by_xpath("//input[@value='搜公众号']").click()
            time.sleep(random.uniform(3, 4))
            element = driver.find_element_by_xpath("//a[@uigs='account_name_0']").click()
            # window_elements = driver.find_elements_by_xpath("//div[@class='txt-box']/p/a")
            # for e in window_elements:
            #     e.click()
            time.sleep(random.uniform(1, 2))
            base_handle = driver.current_window_handle
            for handle in driver.window_handles:
                if handle != base_handle:
                    driver.switch_to.window(handle)
                    elements = driver.find_elements_by_class_name("weui_media_bd")
                    num = len(elements)
                    for i in range(3):
                        bd = driver.find_elements_by_class_name("weui_media_bd")
                        try:
                            publish_time = bd[i].find_element_by_class_name("weui_media_extra_info").text
                            elements = driver.find_elements_by_class_name("weui_media_title")
                            elements[i].click()
                            title = driver.find_element_by_class_name("rich_media_title").text
                            content = driver.find_element_by_id("js_content").text
                            print("title:", title)
                        except (NoSuchElementException, IndexError) as e:
                            print("更换代理")
                            break
                        time.sleep(random.uniform(1, 3))
                        driver.back()
                    driver.quit()
                    driver.close()
            driver.switch_to.window(base_handle)
            time.sleep(random.uniform(1, 2))
    driver.quit()
    driver.close()


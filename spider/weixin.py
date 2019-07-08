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
    # driver = webdriver.Chrome('C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver')
    driver = webdriver.Chrome('/Users/mac/software/chromedriver')
    query_url = "https://weixin.sogou.com/weixin?type=1&query={}&ie=utf8&s_from=input&_sug_=y&_sug_type_=".format("石油")
    driver.get(url)
    driver.find_element_by_id("query").send_keys("python")
    driver.find_element_by_xpath("//input[@value='搜公众号']").click()
    # element = driver.find_element_by_xpath("//a[@uigs='account_name_0']").click()
    element = driver.find_element_by_xpath("//div[@class='txt-box']/p/a")
    for e in element:
        e.click()
    time.sleep(1)
    base_handle = driver.current_window_handle
    for handle in driver.window_handles:
        if handle != base_handle:
            driver.switch_to.window(handle)
            elements = driver.find_elements_by_class_name("weui_media_bd")
            num = len(elements)
            for i in range(len(elements)):
                bd = driver.find_elements_by_class_name("weui_media_bd")
                publish_time = bd[i].find_element_by_class_name("weui_media_extra_info").text
                elements = driver.find_elements_by_class_name("weui_media_title")
                print("进入公众号文章页面")
                elements[i].click()
                try:
                    title = driver.find_element_by_class_name("rich_media_title").text
                    content = driver.find_element_by_id("js_content").text
                    print("title:", title)
                except NoSuchElementException as e:
                    print()
                time.sleep(3)
                driver.back()
            driver.close()
    driver.switch_to.window(base_handle)
    time.sleep(3)
    driver.close()


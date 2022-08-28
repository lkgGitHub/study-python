import datetime
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


# 2010年1月1日至2022年8月9日间数据，输入数据为期间每日的 9点30分和13点1分
def qi_men(t: datetime):
    yearElement = driver.find_element_by_xpath("//select[@name='Year']")
    all_options = yearElement.find_elements_by_tag_name("option")
    for option in all_options:
        attributeValue = option.get_attribute("value")
        if int(attributeValue) == t.year:
            option.click()
            break

    monthElement = driver.find_element_by_xpath("//select[@name='Month']")
    all_options = monthElement.find_elements_by_tag_name("option")
    for option in all_options:
        attributeValue = option.get_attribute("value")
        if int(attributeValue) == t.month:
            option.click()
            break

    dayElement = driver.find_element_by_xpath("//select[@name='Day']")
    all_options = dayElement.find_elements_by_tag_name("option")
    for option in all_options:
        attributeValue = option.get_attribute("value")
        if int(attributeValue) == t.day:
            option.click()
            break

    hourElement = driver.find_element_by_xpath("//select[@name='Hour']")
    all_options = hourElement.find_elements_by_tag_name("option")
    for option in all_options:
        attributeValue = option.get_attribute("value")
        if int(attributeValue) == t.hour:
            option.click()
            break

    submitElement = driver.find_element_by_xpath("//input[@name='Submit']")
    submitElement.click()
    time.sleep(0.5)
    e = driver.find_element_by_xpath("/html/body/table/tbody/tr/td")
    with open(f"result/{ t.strftime('%Y年%m月%d日%H点')}.txt", 'w') as f:
        f.write(e.text)
    print(e.text)
    driver.back()


driver = webdriver.Chrome()

if __name__ == '__main__':
    options = webdriver.ChromeOptions()
    # options.binary_location = "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"
    options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    # chrome_driver_binary = "/usr/local/bin/chromedriver"
    driver = webdriver.Chrome(options=options)
    driver.get("http://pp.qg108.com/qimen/")

    now = datetime.datetime.now()
    startStr = "2010年1月1日9点"
    start = datetime.datetime.strptime(startStr, '%Y年%m月%d日%H点')
    # endStr = "2022年8月9日13点"
    endStr = "2010年1月3日9点"
    end = datetime.datetime.strptime(endStr, '%Y年%m月%d日%H点')
    while start <= end:
        start = start.replace(hour=9)
        qi_men(start)
        start = start.replace(hour=13)
        qi_men(start)
        start = start + datetime.timedelta(days=1)
    driver.close()

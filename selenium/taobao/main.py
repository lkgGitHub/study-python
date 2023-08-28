import datetime
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


if __name__ == '__main__':
    startTime = datetime.datetime.now()
    options = webdriver.ChromeOptions()
    # options.binary_location = "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"
    options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    # chrome_driver_binary = "/Users/lkg/software/bin/chromedriver"
    driver = webdriver.Chrome(options=options)
    driver.get("https://m.tb.cn/h.U3jixwe")

    time.sleep(60)
    driver.close()
    print(f"spend time {datetime.datetime.now() - startTime}")
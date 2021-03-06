# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
# See documentation in: https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import requests
import logging
import json
import time
from scrapy import signals
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .settings import COOKIES_FILE_PATH, chromedriver_path


class ScrapyspiderSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # 当你初见spiders时候调用这个方法。This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        """在下载器中间件处理完成后，马上要进入某个回调函数parse_xxx()前调用"""
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        """当运行到yield scrapy.Request()或者yield item的时候, 被调用"""
        # Called with the results returned from the Spider, after it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        """ 当出现异常时将被调用"""
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        """ 当运行到start_requests()的时候,被调用"""
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ScrapyspiderDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


# class UserAgentMiddleware2(UserAgentMiddleware):


class ProxyMiddleware(object):
    """代理中间件"""

    def process_request(self, request, spider):
        boo = False
        proxy = ""
        for i in range(10):
            p = requests.get("http://127.0.0.1:5010/get/").content
            if isinstance(p, bytes):
                p = p.decode('utf8')
            proxy = "http://{proxy}".format(proxy=p)
            try:
                r = requests.get('http://httpbin.org/ip', proxies={"http": proxy}, timeout=3, verify=False)
                if r.status_code == 200 and r.json().get("origin"):
                    boo = True
                    break
                else:
                    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))
            except Exception as e:
                print(e)
                print("代理ip失败:{}".format(proxy))
                requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))
        if boo:
            print(proxy)
            request.meta['proxy'] = proxy


class CodeMiddleware(object):
    """
        验证码中间件
        遇到验证码时调用selenium进行打码操作
        此处采用人工打码，如果采集数量大的情况建议使用打码平台Api
    """

    def __init__(self):

        self.logger = logging.getLogger(__name__)
        self.new_cookies = {}
        self.login_url = 'https://weixin.sogou.com'
        self.cookies_file_path = COOKIES_FILE_PATH

    def get_browser_cookies(self):
        """
            从本地文件读取cookies，并转换成scrapy.Request的cookies格式
        """

        with open(self.cookies_file_path, 'r') as f:
            listCookie = json.loads(f.read())

        cookies = {}

        # cookies格式转换
        for Cookie in listCookie:
            name = Cookie.get('name')
            value = Cookie.get('value')
            cookies[name] = value
        return cookies

    def process_request(self, request, spider):
        """
            检测Reques对象有没有设置cookies
            如果没有，则调用chrome进行登陆操作，并写入cookies到本地
        """
        if not request.cookies:
            options = webdriver.ChromeOptions()
            # 设置中文
            options.add_argument('lang=zh_CN.UTF-8')
            # 更换头部
            options.add_argument(
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36')
            # browser = webdriver.Chrome(executable_path=chromedriver_path, chrome_options=options)
            browser = webdriver.Chrome(executable_path=chromedriver_path)
            wait = WebDriverWait(browser, 10)

            browser.get(self.login_url)
            time.sleep(1)
            login = wait.until(EC.element_to_be_clickable((By.ID, 'loginBtn')))
            login.click()
            time.sleep(2)
            yzm_image = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="login-pop-wx"]/iframe')))

            yzm_url = yzm_image.get_attribute('src')

            browser.get(yzm_url)
            time.sleep(2)
            # browser.delete_all_cookies()
            input('请完成登陆，然后回车～')

            listCookie = browser.get_cookies()
            self.logger.debug('[+] Chrome cookies is %s' % listCookie)

            with open(self.cookies_file_path, 'w') as f:
                f.write(json.dumps(listCookie))

            browser.close()

            request.cookies = self.get_browser_cookies()

    def process_response(self, request, response, spider):
        """
            重定向处理，response状态码为302
            情况一：调用Chrome访问重定向页面为验证码页面，则输入验证码，获取新cookies，并返回带有新cookies值的Request
            情况二：调用Chrome访问重定向页面为正常页面，则保存新cookies，并返回带有新cookies值的Request
            一般微信的反爬为第一次重定向页面为第二种情况，后续为情况一
        """
        if response.status == 302:
            url = response.url
            # proxy = request.meta['proxy']
            self.logger.debug('[+] url:%s,status:%s' % (url, response.status))
            # self.logger.debug('[+] request_url is : %s' % request.url)
            '''设置代理浏览器'''
            chrome_options = webdriver.ChromeOptions()
            # chrome_options.add_argument('--proxy-server='+proxy)
            time.sleep(2)
            browser = webdriver.Chrome(executable_path=chromedriver_path, chrome_options=chrome_options)
            wait = WebDriverWait(browser, 15)
            time.sleep(2)
            # 需要先打开页面才能设置cookeis
            browser.get('https://weixin.sogou.com')
            browser.delete_all_cookies()
            time.sleep(3)

            '''设置selenium浏览器的cookie'''
            with open(self.cookies_file_path, 'r') as f:
                listCookie = json.loads(f.read())
            time.sleep(1)
            for cookie in listCookie:
                browser.add_cookie({
                    'domain': cookie['domain'],
                    'httpOnly': cookie['httpOnly'],
                    'name': cookie['name'],
                    'path': cookie['path'],
                    'secure': cookie['secure'],
                    'value': cookie['value'],
                    'expiry': None if 'expiry' not in cookie else cookie['expiry']
                })

            if not browser.get(url):
                # 进行页面判定，如果不是not Found页面，则进行后续操作
                try:
                    test = browser.find_element_by_xpath('//div[@id="main-message"]/h1/span').text
                except:
                    test = False
                if test:
                    self.logger.debug('[+] proxy is broken')
                    browser.close()
                    return request

                # from scrapy.shell import inspect_response
                # inspect_response(response,spider)

                # 获取验证码文本框
                self.logger.debug('[!] search input_text ....')
                try:
                    input_text = wait.until(EC.presence_of_element_located((By.ID, 'seccodeInput')))
                    self.logger.debug('[√] input_text done!')
                except:
                    self.logger.debug('[!] input_text fail !')
                    input_text = None

                # 判断是情况一还是情况二，如果情况一则直接返回带有新cookies值的Request
                if input_text:

                    # 获取提交验证码的button
                    self.logger.debug('[!] search button....')
                    try:
                        button = wait.until(EC.element_to_be_clickable((By.ID, 'submit')))
                        self.logger.debug('[√] button done!')
                    except:
                        self.logger.debug('[!] button fail!')

                    code = str(input('please input code:'))

                    input_text.clear()
                    time.sleep(3)
                    if not input_text.send_keys(code):
                        # 这里停顿3秒才按button是模仿人为操作
                        time.sleep(3)
                        if not button.click():

                            time.sleep(3)

                            # 设置新cookie
                            self.logger.debug('[+] Set new cookies: ')
                            new_listCookie = browser.get_cookies()

                            with open(self.cookies_file_path, 'w') as f:
                                f.write(json.dumps(new_listCookie))

                            self.logger.info('[+] This is new_listCookie: %s' % new_listCookie)
                            for cookie in new_listCookie:
                                name = cookie.get('name')
                                value = cookie.get('value')
                                self.new_cookies[name] = value

                else:
                    new_listCookie = browser.get_cookies()
                    self.logger.info('[+] This is new_listCookie: %s' % new_listCookie)
                    for cookie in new_listCookie:
                        name = cookie.get('name')
                        value = cookie.get('value')
                        self.new_cookies[name] = value

                    # request.meta['retry_times'] = False

                browser.close()
                request.cookies = self.new_cookies
                return request
                '''
                page = request.meta.get('page')
                word = request.meta.get('word')
                cookie = request.cookies
                t = request.callback
                return scrapy.Request(url=url,callback=t,cookies=cookie,meta={'page':page,'word':word,'proxy':proxy},dont_filter=True)
                '''

                # return request.replace(url = url)

        else:
            self.logger.debug('[+] 200 Continue.......')
            return response

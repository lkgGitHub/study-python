# -*- coding: utf-8 -*-

# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

LOG_LEVEL = 'INFO'  # CRITICAL, ERROR, WARNING, INFO, DEBUG
# url 去重过滤类
# DUPEFILTER_CLASS = 'scrapySpider.filter.RedisBloomFilter'
# 爬取网站最大允许的深度(depth)值。如果为0，则没有限制。（默认: 0）
DEPTH_LIMIT = 5
BOT_NAME = 'scrapySpider'

SPIDER_MODULES = ['scrapySpider.spiders']
NEWSPIDER_MODULE = 'scrapySpider.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'scrapySpider (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# 下载器在下载同一个网站下一个页面前需要等待的时间。该选项可以用来限制爬取速度。同时也支持小数。默认：0
DOWNLOAD_DELAY = 0

# 对单个网站进行并发请求的最大值,默认为8:
CONCURRENT_REQUESTS_PER_DOMAIN = 1

# 下载器超时时间(单位: 秒)。
DOWNLOAD_TIMEOUT = 10

# 是否启用cookie中间件(默认启动）
COOKIES_ENABLED = True

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# 重写请求headers （Override the default request headers）
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# 爬虫中间件（Spider Middleware）【https://doc.scrapy.org/en/latest/topics/spider-middleware.html】
# SPIDER_MIDDLEWARES = {
#    'scrapySpider.middlewares.ScrapyspiderSpiderMiddleware': 543,
# }

# 下载中间件（downloader middlewares）【https://doc.scrapy.org/en/latest/topics/downloader-middleware.html】
# 作用：更换代理IP，更换Cookies，更换User-Agent，自动重试。。数字越小的中间件越先执行
# DOWNLOADER_MIDDLEWARES = {
#    # 'scrapySpider.middlewares.UserAgentMiddleware': 544,
#    'scrapySpider.middlewares.ProxyMiddleware': 811  # 代理中间件
#    # 'scrapySpider.middlewares.CodeMiddleware': 812,
# }

#  扩展(extensions) 【https://doc.scrapy.org/en/latest/topics/extensions.html】
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    'scrapySpider.pipelines.CsvPipeline': 300,
#    'scrapySpider.pipelines.JsonWriterPipeline': 300,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# 自定义配置
COOKIES_FILE_PATH = 'cookies.json'
# chromedriver_path = '/Users/mac/software/chromedriver'
chromedriver_path = 'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver'

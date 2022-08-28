# -*- coding: utf-8 -*-

#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

# 自定义配置
# mysql 配置
MYSQL_DB_NAME = 'nd'
MYSQL_HOST = '127.0.0.1'
MYSQL_USER = 'root'
MYSQL_PASSWORD = '123456'
#############################################################################################

BOT_NAME = 'nd'

SPIDER_MODULES = ['nd.spiders']
NEWSPIDER_MODULE = 'nd.spiders'

LOG_LEVEL = 'DEBUG'  # CRITICAL, ERROR, WARNING, INFO, DEBUG

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'nd (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# 下载器在下载同一个网站下一个页面前需要等待的时间。该选项可以用来限制爬取速度。同时也支持小数。默认：0
DOWNLOAD_DELAY = 0
# 对单个网站进行并发请求的最大值,默认为8:
CONCURRENT_REQUESTS_PER_DOMAIN = 8
# CONCURRENT_REQUESTS_PER_IP = 16

# 是否启用cookie中间件(默认启动）
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# 重写请求headers （Override the default request headers）
DEFAULT_REQUEST_HEADERS = {
    "Accept-Encoding": "gzip, deflate, br",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/78.0.3904.108 Safari/537.36 "
}

# 爬虫中间件（Spider Middleware）【https://doc.scrapy.org/en/latest/topics/spider-middleware.html】
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'nd.middlewares.NiuDunSpiderMiddleware': 543,
# }

# 下载中间件（downloader middlewares）【https://doc.scrapy.org/en/latest/topics/downloader-middleware.html】
# 作用：更换代理IP，更换Cookies，更换User-Agent，自动重试。。数字越小的中间件越先执行
# DOWNLOADER_MIDDLEWARES = {
#    'nd.middlewares.NiuDunDownloaderMiddleware': 543,
# }

# 扩展(extensions) 【https://doc.scrapy.org/en/latest/topics/extensions.html】
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'nd.pipelines.MySQLPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
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
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

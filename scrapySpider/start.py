from scrapy import cmdline

# cmdline.execute("scrapy crawl ftchinese".split())
cmdline.execute("scrapy crawl sogou_weixin0 -o filename.csv".split())

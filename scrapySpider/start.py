from scrapy import cmdline

cmdline.execute("scrapy crawl ifeng -o news.csv".split())
cmdline.execute("scrapy crawl yicai -o news.csv".split())
# cmdline.execute("scrapy crawl ftchinese -o news.csv".split())
# cmdline.execute("scrapy crawl sogou_weixin0 -o filename.csv".split())

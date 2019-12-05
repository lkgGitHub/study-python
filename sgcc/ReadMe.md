# sgcc 国家电网
1. 元搜索,网站的链接的发现与识别
2. 针对ZoomEye、Shodan等公司的网络资产扫描服务所发现的网络资产数
3. 流浪镜像做流量探测与识别资产
4. 针对网络泄露数据发现。例如：网盘、文库、github
5. 针对网络上相关的APP应用发现
6. 针对网络上相关的微信公众号发现

```shell script
# 创建项目
scrapy startproject sgcc
# 创建爬虫
scrapy genspider MetaSearch MetaSearch.com
```

 

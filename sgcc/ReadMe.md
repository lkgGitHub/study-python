# sgcc 国家电网
# 任务
- [ ] 1.元搜索,网站的链接的发现与识别
- [ ] 2.针对ZoomEye、Shodan等公司的网络资产扫描服务所发现的网络资产数
- [ ] 3.流浪镜像做流量探测与识别资产
- [ ] 4.针对网络泄露数据发现。
    - [ ] 4.1:网盘
    - [ ] 4.2:文库
    - [ ] 4.3:github
- [ ] 5.针对网络上相关的APP应用发现
- [x] 6.针对网络上相关的微信公众号发现


```shell script
# 创建项目
scrapy startproject sgcc
# 创建爬虫
scrapy genspider MetaSearch MetaSearch.com
```

 

# sgcc 国家电网

# 任务
- [x] 1.元搜索,网站的链接的发现与识别
    - [x] 1.1 百度
    - [ ] 1.2 搜狗
- [x] 2.针对ZoomEye、Shodan等公司的网络资产扫描服务所发现的网络资产数
    - [x] 2.1 ZoomEye
    - [x] 2.2 Shodan
    - [x] 2.3 Fofa
- [ ] 3.流量镜像做流量探测与识别资产
- [x] 4.针对网络泄露数据发现。
    - [x] 4.1 网盘
    - [x] 4.2 文库
    - [x] 4.3 github
    - [ ] 4.4 豆丁
    - [ ] 4.5 gitee
- [x] 5.针对网络上相关的APP应用发现
- [x] 6.针对网络上相关的微信公众号发现

- [ ] 数据库设计
- [ ] 疑似分析与初步判定
- [ ] 图像处理
- [ ] 黑白名单
- [ ] 底层监控与守护
- [ ] 日志组件
- [ ] 前端操作页面


```shell script
# 创建项目
scrapy startproject sgcc
# 创建爬虫
scrapy genspider MetaSearch MetaSearch.com
```

 

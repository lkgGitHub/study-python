from scrapy import cmdline

# -o weixin.csv
# cmdline.execute("scrapy crawl wechat".split())
cmdline.execute("scrapy crawl sogou".split())

# cmdline.execute("scrapy crawl wenku".split())
# cmdline.execute("scrapy crawl baidu".split())
# cmdline.execute("scrapy crawl panSou".split())
# cmdline.execute("scrapy crawl huawei".split())

def insert_mysql():
    import pymysql
    db_conn = pymysql.connect(host='localhost', port=3306, db='nd', user='root', passwd='123456', charset='utf8')
    db_cur = db_conn.cursor()
    keyword = []
    with open('keyword.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            keyword.append(line.strip())

    with open('keyword1.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            keyword.append(line.strip())

    with open('keyword2.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            keyword.append(line.strip())

    sql = "INSERT INTO keyword (keyword.`keyword`) VALUES (%s)"
    values = set(keyword)
    db_cur.executemany(sql, values)
    db_conn.commit()
    db_cur.close()
    db_conn.close()

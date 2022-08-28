import pymysql


if __name__ == '__main__':
    connect = pymysql.Connect(host='127.0.0.1', user='root', password='123456', database='bootdo', charset='utf8')
    # 获取游标
    cursor = connect.cursor()

    # 执行查询 SQL
    cursor.execute('SELECT * FROM `sys_user`')

    # 获取单条数据
    one = cursor.fetchone()
    # 获取前N条数据
    many = cursor.fetchmany(3)
    # 获取所有数据
    allData = cursor.fetchall()

    print("one:", one)
    print("many:", many)
    print("allData:", allData)

    # 关闭数据库连接
    connect.close()

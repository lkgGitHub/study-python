import redis
# 安装：conda install redis-py

if __name__ == '__main__':
    r = redis.Redis(host='localhost', port=6379, db=0)
    b = r.set('foo', 'bar')
    r.get('foo')
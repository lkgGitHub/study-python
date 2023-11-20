import redis
from redis import ResponseError
from scrapy.dupefilters import RFPDupeFilter
import logging


class RedisBloomFilter(RFPDupeFilter):
    """ redis布隆过滤器，只根据url去重"""
    def __init__(self, path=None, debug=False):
        logging.info("init redis bloomFilter")
        self.key = "url"
        self.redis_client = redis.Redis(host='127.0.0.1', port=6379)
        error_rate = 0.001
        initial_size = 1000
        try:
            # bf.reserve，提供了三个参数， key, error_rate和initial_size。错误率越低，需要的空间越大，initial_size
            # 参数表示预计放入布隆过滤器的元素数量，当实际数量超出这个数值时，误判率会上升。 默认的参数是 error_rate=0.01, initial_size=100。
            self.redis_client.execute_command("bf.reserve", self.key, error_rate, initial_size)
        except ResponseError as e:
            logging.info(e)

        RFPDupeFilter.__init__(self, path)

    def request_seen(self, request):
        boo = self.redis_client.execute_command("bf.exists", self.key, request.url)
        if boo:
            return True
        else:
            self.redis_client.execute_command("bf.add", self.key, request.url)


class SeenURLFilter(RFPDupeFilter):
    """只根据url去重"""
    def __init__(self, path=None):
        self.urls_seen = set()
        RFPDupeFilter.__init__(self, path)

    def request_seen(self, request):
        if request.url in self.urls_seen:
            return True
        else:
            self.urls_seen.add(request.url)


if __name__ == '__main__':
    client = redis.Redis(host='127.0.0.1', port=6379)
    client.delete("url")
    size = 1000
    count = 0
    # bf.reserve，提供了三个参数， key, error_rate和initial_size。错误率越低，需要的空间越大，initial_size
    # 参数表示预计放入布隆过滤器的元素数量，当实际数量超出这个数值时，误判率会上升。 默认的参数是 error_rate=0.01, initial_size=100。
    client.execute_command("bf.reserve", "url", 0.001, size)  # 新增
    for i in range(size):
        client.execute_command("bf.add", "tiancheng", "tc%d" % i)
        result = client.execute_command("bf.exists", "tiancheng", "tc%d" % (i + 1))
        if result == 1:
            print(i)
            count += 1

    print("size: {} , error rate: {}%".format(
        size, round(count / size * 100, 5)))

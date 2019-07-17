import redis

if __name__ == '__main__':
    client = redis.Redis(host='127.0.0.1', port=6379)
    client.delete("tiancheng")
    size = 100000
    count = 0
    # bf.reserve，提供了三个参数， key, error_rate和initial_size。错误率越低，需要的空间越大，initial_size
    # 参数表示预计放入布隆过滤器的元素数量，当实际数量超出这个数值时，误判率会上升。 默认的参数是 error_rate=0.01, initial_size=100。
    client.execute_command("bf.reserve", "tiancheng", 0.001, size)  # 新增
    for i in range(size):
        client.execute_command("bf.add", "tiancheng", "tc%d" % i)
        result = client.execute_command("bf.exists", "tiancheng", "tc%d" % (i + 1))
        if result == 1:
            # print(i)
            count += 1

    print("size: {} , error rate: {}%".format(
        size, round(count / size * 100, 5)))


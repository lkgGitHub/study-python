

# redis 安装
```shell
# 安装依赖
sudo apt install make gcc
# 下载安装
wget http://download.redis.io/releases/redis-5.0.5.tar.gz
tar xzf redis-5.0.5.tar.gz
cd redis-5.0.5
make MALLOC=libc
# 修改配置文件redis.conf，启动
src/redis-server redis.conf
```
## RedisBloom 安装
```shell
# branch参数指定克隆的tag。
git clone --branch v2.0.2 https://github.com/RedisBloom/RedisBloom.git 
cd RedisBloom
make
# loadmodule 加载自定义module，也可以在redis.conf中
src/redis-server --loadmodule .RedisBloom/redisbloom.so
```
### RedisBloom命令
```shell
# 设置
BF.RESERVE {key} {error_rate} {capacity}
# 添加
BF.ADD {key} {item}
BF.MADD {key} {item} [item...]
# 检验是否存在
BF.EXISTS {key} {item}
BF.MEXISTS {key} {item} [item...]
```
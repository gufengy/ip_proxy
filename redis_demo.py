import redis   # 导入redis模块，通过python操作redis 也可以直接在redis主机的服务端操作缓存数据库

Host = '127.0.0.1'
Port = 6379

# 使用redis连接池
pool = redis.ConnectionPool(host=Host, port=Port, decode_responses=True)   # host是redis主机，需要redis服务端和客户端都起着 redis默认端口是6379
r = redis.Redis(connection_pool=pool)
# r.set('name', 'junxi')  # key是"foo" value是"bar" 将键值对存入redis缓存
# print(r['name'])
# print(r.get('name'))  # 取出键name对应的值
# print(type(r.get('name')))


# 测试有序不重复集合Set
r.zadd("zset2", 'm1', 22, 'm2', 44)

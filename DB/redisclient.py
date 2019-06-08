import redis   # 导入redis模块，通过python操作redis 也可以直接在redis主机的服务端操作缓存数据库
import random

Host = '127.0.0.1'
Port = 6379
Sort_Set = 'ip_proxy'
Max_Score = 10

'''
redis中的hashmap 的数据key是不能重复的
'''
class redisclient(object):

    def __init__(self):
        self.r = self.get_redis_connect()

    '''
    获取redis数据连接池的一个连接
    '''
    def get_redis_connect(self):
        pool = redis.ConnectionPool(host=Host, port=Port,
                                    decode_responses=True)  # host是redis主机，需要redis服务端和客户端都起着 redis默认端口是6379
        return redis.Redis(connection_pool=pool)

    '''
    根据键值的形式向redis中添加信息
    :key_type 设置数据库名
    :key 向redis中添加键, 这个键使用 ip 地址作为键
    :score 添加的分数, 第一次插入数据的分数为 9 
    '''
    def add(self, key, score):
        self.r.zadd(key[0:5].replace(":", ""), {str(key): score})

    # '''
    # 获取根据键获取一个代理信息
    # '''
    # def get_value(self, key):
    #     return self.r.hget(Hash_Name, key)

    '''
    随机获取一个高可用的代理信息
    '''
    def get_random_proxy(self):
        return self.get_proxy_keyong()

    '''
    获取一个可用的代理数据量
    '''
    def get_proxy_keyong(self):
        http_proxy = self.r.zrangebyscore("http", Max_Score, Max_Score)
        https_proxy = self.r.zrangebyscore("https", Max_Score, Max_Score)
        # 在http类型和代理中和 https类型的代理中个获取一个随机的代理, 放到字典中 return 出去
        return {"http": http_proxy[random.randint(0, len(http_proxy)-1)], "https": https_proxy[random.randint(0, len(https_proxy)-1)]}

    '''
    根据key删除一条数据数据
    '''
    def del_proxy(self, key):
        self.r.zrem(key[0:5].replace(":", ""), key)

    '''
    获取数据库中的所有元素包括分数
    '''
    def get_all_proxy(self):
        # 获取数据库中的元素和分数, 倒叙
        # return self.r.zrange(Sort_Set, 0, -1, withscores=True)
        # 获取数据库中的元素和分数, 正序
        result1 = self.r.zrange("http", 0, -1, desc=True, withscores=True)
        result2 = self.r.zrange("https", 0, -1, desc=True, withscores=True)
        return result1 + result2

    '''
    获取数据库中的所有元素不包括分数
    '''
    def get_proxy_keys(self, ip_type):
        return self.r.zrange(ip_type, 0, -1)

    '''
    根据传入的ip检测在redis中是否已经添加了该ip的信息, 返回值为boolean类型数据
    存在 True
    不存在 False
    '''
    def proxy_exist(self, ip, ip_type):
        return ip in self.get_proxy_keys(ip_type)

    '''根据key获取一个ip的分数'''
    def get_score_by_key(self, ip_type, key):
        return self.r.zscore(ip_type, key)


    '''
    根据传入的元祖类型的数据对数据库中的数据进行维护, 减分
    '''
    def minus_score(self, proxy):
        ip_type = proxy[0:5].replace(":", "")
        proxy_score = self.get_score_by_key(ip_type, proxy)
        if proxy_score > 1:
            self.add(proxy, proxy_score-1)
        elif proxy_score <=1:
            self.del_proxy(proxy)

    def main(self):
        print(self.get_proxy_keys("http"))
        pass



if __name__ == '__main__':
    pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
    r = redis.Redis(connection_pool=pool)
    redisclient().main()
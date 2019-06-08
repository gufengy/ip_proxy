from Config import Control
from multiprocessing.dummy import Pool

MAX_SAVE_NUM = 100  # 数据库中最大的存入数量


class Manager(object):
    def __init__(self):
        self.r = Control.get_redis_client()  # 获取数据库存储对象
        self.pro = Control.get_check_proxy()  # 获取 代理检测对象
        self.p = Control.get_ip_proxy()  # 获取代理获取对象
        self.proxy_func_list = Control.get_ip_proxy().proxy_list
        self.logger = Control.get_logger(__name__)

    def main(self):
        # print(self.proxy_func_list)
        proxy_list = self.p.proxy_list
        for proxy in proxy_list:
            func = getattr(self.p, proxy)
            for ip_proxy in func():
                print(ip_proxy)

    '''
    设置一个保存数据的函数, 新加入的数据分数为9, 测试完成之后
    :proxy_list 查询到的ip列表
    :proxy_num 缺少的ip的数量
    '''

    def save_proxy(self, proxy_list, proxy_num):
        flag = False
        for proxy in proxy_list:
            result = self.r.proxy_exist(proxy, proxy[0:5].replace(":", ""))
            if proxy_num['http'] <= 0 and proxy_num['https'] <= 0:
                self.logger.info("数据量充足")
                break  # 数据量足够, 结束添加
            if not result:
                if proxy[0:5].replace(":", "") == "http" and proxy_num["http"] > 0:
                    self.r.add(proxy, 9)
                    proxy_num["http"] = proxy_num["http"] - 1
                    self.logger.info("成功添加ip:\t" + proxy + "\t当前分数为9")
                elif proxy[0:5].replace(":", "") == "https" and proxy_num["https"] > 0:
                    self.r.add(proxy, 9)
                    proxy_num["https"] = proxy_num["https"] - 1
                    self.logger.info("成功添加ip:\t" + proxy + "\t当前分数为9")
            else:
                flag = True
        return flag

    '''
    定时检查数据库, 如果数据库中的数据量不满足某个设定的值, 那么将会对网站进行爬取, 抓取网站的数据添加数据库
    当不满足数据量的时, 会调用抓取模块, 然后对抓取到的数据进行判断. 判断数据在数据库中是否存在, 如果存在那么舍弃该数据, 如果不存在将添加数据到数据库.
    循环添加数据, 在循环外设置一个flag, 对添加添加数据库成功的进行计数, 当值和数据库中缺失值的数量相同的时候通知循环.
    '''

    def check_db(self):
        I = iter(range(len(self.proxy_func_list)))
        while True:
            self.logger.info('开始检查数据库')
            flag = False
            http_count = MAX_SAVE_NUM - len(self.r.get_proxy_keys("http"))
            https_count = MAX_SAVE_NUM - len(self.r.get_proxy_keys("https"))
            if max(http_count, https_count) > 0:
                self.logger.info("开始添加数据, 本次大概添加数据量为http: %s, https: %s" % (
                str(http_count if (http_count > 0) else 0), str(https_count if (https_count > 0) else 0)))
                func = getattr(self.p, self.proxy_func_list[next(I)])  # 使用python 反射原理获取一个python的可执行方法
                flag = self.save_proxy(func(), {"http": http_count, "https": https_count})
            if not flag:
                self.logger.info("数据量已经是最大值了")
                break

    '''
    检查代理可用性
    '''

    def check_proxy(self):
        proxys = self.r.get_all_proxy()
        pool = Pool(8)
        pool.map(self.pro.check_proxy, proxys)
        pool.close()
        pool.join()

    '''
    获取一个随机的代理
    '''

    def get_proxy_info(self):
        return self.r.get_random_proxy()

    '''
    获取可用的代理数量
    '''

    def get_proxy_keyong(self):
        return len(self.r.get_proxy_keyong())


if __name__ == '__main__':
    app = Manager()
    app.check_db()
    # app.check_proxy()
    # app.main()

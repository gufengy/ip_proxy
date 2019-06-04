from Config import Control
from multiprocessing.dummy import Pool

MAX_SAVE_NUM = 100  # 数据库中最大的存入数量


class Manager(object):
    def __init__(self):
        self.r = Control.get_redis_client()  # 获取数据库存储对象
        self.pro = Control.get_check_proxy()  # 获取 代理检测对象
        self.p = Control.get_ip_proxy()  # 获取代理获取对象
        self.proxy_func_list = Control.get_ip_proxy().proxy_list
        self.logger = Control.get_logger()

    def main(self):
        # print(self.proxy_func_list)
        proxy_list = self.p.proxy_list
        for proxy in proxy_list:
            func = getattr(self.p, proxy)
            for ip_proxy in func():
                print(ip_proxy)

    # 设置一个保存数据的函数, 新加入的数据分数为9, 测试完成之后
    def save_proxy(self, proxy_list):
        flag = False
        for proxy in proxy_list:
            result = self.r.proxy_exist(proxy, proxy[0:5].replace(":", ""))
            if min(len(self.r.get_proxy_keys("http")), len(self.r.get_proxy_keys("https"))) >= MAX_SAVE_NUM:
                self.logger.info("数据量充足")
                break   # 数据量足够, 结束添加
            if not result:
                self.r.add(proxy, 9, proxy[0:5].replace(":", ""))  # 如果数据不存在那么将会把刚刚抓取的数据存入数据库, 并且分数设置为9, 设置为9是为了怕这个 代理没有检测就把它设置为了可以取出的状态了
                self.logger.info("成功添加ip:     " + proxy + "    当前分数为9")
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
            if min(len(self.r.get_proxy_keys("http")), len(self.r.get_proxy_keys("https"))) < MAX_SAVE_NUM:
                self.logger.info("开始添加数据, 本次大概添加数据量为  %s  个" % str(MAX_SAVE_NUM-min(len(self.r.get_proxy_keys("http")), len(self.r.get_proxy_keys("https")))))
                func = getattr(self.p, self.proxy_func_list[next(I)])  # 使用python 反射原理获取一个python的可执行方法
                flag = self.save_proxy(func())
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
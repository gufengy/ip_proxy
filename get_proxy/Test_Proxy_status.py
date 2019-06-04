from redisclient import redisclient
from logger import logger
from fake_useragent import UserAgent
import requests
from requests.exceptions import *
import time



Max_score = 10

class Test_proxy_status(object):

    def __init__(self):
        self.redis = redisclient()
        self.TEST_URL = {"http": "http://ipv4.icanhazip.com/", "https": "https://ipv4.icanhazip.com/"}
        self.logger = logger(__name__)

    '''
    使用requests检测代理可用性
    :proxy 传入的代理和分数, 数据类型为元组, (ip, score)
    '''
    def check_proxy(self, proxy):
        score = int(proxy[1])
        proxy = proxy[0]
        ip_type = proxy[0:5].replace(":", "")
        proxies = {
            ip_type: proxy
        }
        try:
            self.logger.info('正在测试代理:     ' + proxy)
            time.sleep(5)
            response = requests.get(self.TEST_URL[ip_type], headers={'user-agent': UserAgent().random}, timeout=15, proxies=proxies)
            if response.status_code in [200, 502]:
                self.logger.info('代理可用:     ' + proxy)
                self.redis.add(proxy, Max_score, ip_type)
            else:
                self.logger.info('请求响应码不合法!    ' + proxy + "    剩余分数:" + str(score - 1) + "\t响应吗为: " + str(response.status_code))
                self.redis.minus_score(proxy)
        except (ConnectionError ,ConnectTimeout, ReadTimeout, ProxyError, ChunkedEncodingError, SSLError):
            self.logger.info('代理不可用    ' + proxy + "    剩余分数:" + str(score - 1))
            self.redis.minus_score(proxy)
        except Exception as e:
            self.logger.info("没有预料到的异常" + e.args)
            self.logger.info('代理不可用    ' + proxy + "    剩余分数:" + str(score - 1))

    def main(self):
        proxy = "{'ip': '119.101.117.88', 'port': '9999', '匿名度': '高匿名', '类型': 'HTTP', '位置': '湖北省潜江市  电信', '响应速度': '0.6秒', 'score': 10}"
        self.test_proxy(proxy)


if __name__ == '__main__':
    p = Test_proxy_status()
    p.main()
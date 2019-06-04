from fake_useragent import UserAgent
from redisclient import redisclient
import redis
import requests
from requests.exceptions import ConnectTimeout, ReadTimeout, ProxyError
from multiprocessing import Pool

url = "https://ipv4.icanhazip.com/"



#
# for result in result1:
#     result = result[0].lower()
#     proxies = {
#         result[0:5].replace(":", ""): result
#     }
#     print(proxies)
#     try:
#         response = requests.get(url, headers={'user-agent': UserAgent().random}, timeout=15, proxies=proxies)
#         if response.status_code == 200:
#             print(response.text)
#     except (ConnectTimeout, ReadTimeout, ProxyError):
#         print("TimeOut")
#         continue

def check_proxy(proxy):
    proxy = proxy[0].lower()
    proxies = {
        proxy[0:5].replace(":", ""): proxy
    }
    try:
        response = requests.get(url, headers={'user-agent': UserAgent().random}, timeout=15, proxies=proxies)
        if response.status_code == 200:
            print(response.text)
    except (ConnectTimeout, ReadTimeout, ProxyError):
        print(proxy + "     不可用")




# aa = redisclient()
# print(aa.get_all_proxy())

# print(UserAgent().random)
#
# string = 'HTTP://112.85.130.178:9999'
# print(string[0:4])

if __name__ == '__main__':
    r_pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
    r = redis.Redis(connection_pool=r_pool)
    result1 = r.zrange("HTTPS", 0, -1, desc=True, withscores=True)
    pool = Pool(8)
    pool.map(check_proxy, result1)
    pool.close()
    pool.join()
    print("线程结束")
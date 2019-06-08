import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from Config import Control
import time

ip_link1 = "https://www.xicidaili.com/nn/"
# ip_link2 = "https://www.xicidaili.com/nt/"
INIT_SCORE = 10

class Get_Proxy(object):
    def __init__(self):
        self.logger = Control.get_logger(__name__)
        # 设置获取ip的方法名
        self.proxy_list = [
            "parse_page_one",
            "parse_page_two",
            "parse_page_three"
        ]

    def request_get(self, url):
        while True:
            try:
                response = requests.get(url, headers={"user-agent": UserAgent().random}, timeout=15)
                if response.status_code == 200:
                    return response.text
                else:
                    self.logger.warning("请求状态码出错:\t" + url + ", 状态码: \t" + str(response.status_code))
                    time.sleep(10)
            except Exception as e:
                self.logger.error("请求出现异常:\t" + url + ", 异常内容: \t", exc_info=True)
                time.sleep(10)

    '''
    获取神鸡代理ip的首页ip地址
    url = http://www.shenjidaili.com/open/
    '''
    def parse_page_one(self):
        url = "http://www.shenjidaili.com/open/"
        self.logger.info("正在抓取神鸡代理: " + url)
        response = self.request_get(url)
        proxy_list = []
        soup = BeautifulSoup(response, "lxml")
        soup_https = soup.select("#pills-stable_https > table")[0].find_all("tr")
        soup_http = soup.select("#pills-stable_http > table")[0].find_all("tr")
        soup = soup_http + soup_https
        for proxy_info in soup:
            proxy_node = proxy_info.select("td")
            if "端口" in proxy_node[1].string:
                continue
            proxy = proxy_node[3].string.lower() + "://" + proxy_node[0].string
            proxy_list.append(proxy)
        return proxy_list

    '''
    获取ip海里的国内高匿代理
    url = http://www.iphai.com/free/ng
    获取ip海的国外高匿ip代理
    url = http://www.iphai.com/free/wg
    '''
    def parse_page_two(self):
        url_list = ["http://www.iphai.com/free/ng", "http://www.iphai.com/free/wg"]
        proxy_list = []
        for url in url_list:
            self.logger.info("正在抓取ip海代理: " + url)
            response = self.request_get(url)
            soup = BeautifulSoup(response, "lxml")
            soup = soup.find("table", attrs={"class", "table table-bordered table-striped table-hover"}).find_all("tr")
            for proxy_info in soup:
                proxy_node = proxy_info.select("td")
                if proxy_node == []:
                    continue
                ip_type = proxy_node[3].string.strip().lower()
                if ip_type is None or ip_type == "":
                    ip_type = "http"
                proxy_list.append(ip_type + "://" + proxy_node[0].string.strip() + ":" + proxy_node[1].string.strip())
        return proxy_list

    '''
    获取西刺代理, 这个网站的代理质量非常差
    url = https://www.xicidaili.com/nn/
    '''
    def parse_page_three(self):
        url = "https://www.xicidaili.com/nn/1"
        self.logger.info("正在抓取西刺代理: " + url)
        response = self.request_get(url)
        soup = BeautifulSoup(response, 'lxml').find_all('tr', attrs={'class': 'odd'})  # 使用BeautifulSoup格式化代码
        ip_list = []
        for soup_child in soup:
            ip_type = soup_child.select('td')[5].string
            result_ip = ip_type + "://" + soup_child.select('td')[1].string + ":" + soup_child.select('td')[2].string
            ip_list.append(result_ip.lower())
        return ip_list

    def main(self):
        # result = self.parse_page_one()
        # for proxy in result:
        #     print(proxy)
            # print("---------------------------------")
        # result = self.parse_page_three()
        # 使用反射进行执行方法
        proxy_list = self.proxy_list
        i = 1
        for proxy  in proxy_list:
            func = getattr(get_proxy, proxy)
            ip_proxy = func()
            for i in range(len(ip_proxy)):
                print(str(i))
                print(ip_proxy[i])





if __name__ == '__main__':
    get_proxy = Get_Proxy()
    # get_proxy.main()
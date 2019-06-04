from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent

url = "http://www.shenjidaili.com/open/"

if __name__ == '__main__':
    response = requests.get(url, headers={"User-Agent": UserAgent().random})
    proxy_list = []
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "lxml")
        soup_https = soup.select("#pills-stable_https > table")[0].find_all("tr")
        soup_http = soup.select("#pills-stable_http > table")[0].find_all("tr")
        soup = soup_http + soup_https
        for proxy_info in soup:
            proxy_event = proxy_info.select("td")
            if "端口" in proxy_event[1].string:
                continue
            proxy = proxy_event[3].string.lower() + "://" + proxy_event[0].string
            proxy_list.append(proxy)

    test_url = {"http":"http://ipv4.icanhazip.com/", "https": "https://ipv4.icanhazip.com/"}
    for proxy in proxy_list:
        print(proxy)
        ip_type = proxy[0:5].replace(":","")
        requests.get(test_url[ip_type], timeout=15, proxies={ip_type: proxy}, headers={"User-Agent": UserAgent().random})
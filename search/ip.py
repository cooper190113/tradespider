import requests
from lxml import etree
import time
import json

#https://www.cnblogs.com/supershuai/p/12297312.html
def get_all_proxy(page):
    url = 'https://www.xicidaili.com/nn/%s' % page
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    }
    response = requests.get(url, headers=headers)
    html_ele = etree.HTML(response.text)
    ip_eles = html_ele.xpath('//table[@id="ip_list"]/tr/td[2]/text()')
    port_ele = html_ele.xpath('//table[@id="ip_list"]/tr/td[3]/text()')
    print(ip_eles)
    proxy_list = []
    for i in range(0, len(ip_eles)):
        check_all_proxy(ip_eles[i], port_ele[i])
    return proxy_list


def check_all_proxy(host, port):
    type = 'http'
    proxies = {}
    proxy_str = "%s://@%s:%s" % (type, host, port)
    valid_proxy_list = []
    url = 'http://www.baidu.com/'
    proxy_dict = {
        'http': proxy_str,
        'https': proxy_str
    }
    try:
        start_time = time.time()
        response = requests.get(url, proxies=proxy_dict, timeout=5)
        if response.status_code == 200:
            end_time = time.time()
            print('代理可用：' + proxy_str)
            print('耗时:' + str(end_time - start_time))
            proxies['type'] = type
            proxies['host'] = host
            proxies['port'] = port
            proxiesJson = json.dumps(proxies)
            with open('verified_y.json', 'a+') as f:
                f.write(proxiesJson + '\n')
            print("已写入：%s" % proxy_str)
            valid_proxy_list.append(proxy_str)
        else:
            print('代理超时')
    except:
        print('代理不可用--------------->' + proxy_str)


if __name__ == '__main__':
    for i in range(1, 2):  # 选取前十页数据使用
        proxy_list = get_all_proxy(i)
        time.sleep(20)
        print(proxy_list)

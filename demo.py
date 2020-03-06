import time
import urllib.parse

import requests
from requests.exceptions import RequestException


# 百度搜索接口 https://blog.csdn.net/qq_29027865/article/details/84000942
def format_url(url, params: dict = None) -> str:
    query_str = urllib.parse.urlencode(params)
    return f'{url}?{query_str}'


def get_url(keyword):
    params = {
        'wd': str(keyword)
    }
    url = "https://www.baidu.com/s"
    url = format_url(url, params)
    print(url)

    return url


def get_page(url):
    try:
        headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'max-age=0',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
        }
        response = requests.get(url=url, headers=headers)
        time.sleep(3)
        # 更改编码方式，否则会出现乱码的情况
        # response.encoding = "utf-8"
        print(response.status_code)
        # print(response.text)
        if response.status_code == 200:
            return response.content.decode()
        return None
    except RequestException:
        return None

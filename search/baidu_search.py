import csv
import datetime
import os
import random
import sys
import time

from lxml import etree
from selenium import webdriver

from search.config import URL_SEARCH_BAIDU, REFERE, DOMAIN_BAIDU, NEXT_PAGE_FLAG_BAIDU, DRIVER_PATH, LOGGER, PROXY, \
    BLACK_DOMAIN_BAIDU, USER_AGENT

if sys.version_info[0] > 2:
    from urllib.parse import quote_plus, urljoin
else:
    from urllib import quote_plus


class BaiduSpider(object):
    """
    Magic baidu search.
    """

    def __init__(self):
        self.desc = "Baidu"
        self.url = URL_SEARCH_BAIDU
        self.referer = REFERE.format(DOMAIN_BAIDU)

    def search(self, keywords, num, pause=5):
        """
        Get the results you want,such as title,description,url
        :param keywords:
        :param num: pageNum
        :param pause:
        :return: Generator
        """
        self.url = self.url.format(domain=self.get_random_domain(), query=quote_plus(keywords))

        yield ["Title", "Url", "Abstract"]
        for i in range(1, int(num) + 1):
            content = self.search_page(self.url, i, pause)
            for j in range(1, NEXT_PAGE_FLAG_BAIDU):
                data = []
                # 标题
                res_title = content.xpath('//*[@id="%d"]/h3/a' % ((i - 1) * 10 + j))
                title = ""
                if res_title:
                    title = res_title[0].xpath('string(.)')

                # URL
                sub_url = content.xpath('//*[@id="%d"]/h3/a/@href' % ((i - 1) * 10 + j))
                url = ""
                if sub_url:
                    url = sub_url[0]

                # 描述
                res_abstract = content.xpath('//*[@id="%d"]/div[@class="c-abstract"]' % ((i - 1) * 10 + j)) \
                               or content.xpath(
                    '//*[@id="%d"]/div[@class="c-abstract c-abstract-en"]' % ((i - 1) * 10 + j))
                abstract = ""
                if res_abstract:
                    abstract = res_abstract[0].xpath('string(.)')
                else:
                    res_abstract = content.xpath(
                        '//*[@id="%d"]/div/div[2]/div[@class="c-abstract"]' % ((i - 1) * 10 + j)) \
                                   or content.xpath(
                        '//*[@id="%d"]/div/div[2]/div[@class="c-abstract c-abstract-en"]' % ((i - 1) * 10 + j))
                    if res_abstract:
                        abstract = res_abstract[0].xpath('string(.)')

                if not url:
                    continue

                data.append(title)
                data.append(url)
                data.append(abstract)
                yield data

            next_page_index = NEXT_PAGE_FLAG_BAIDU - 1 if i == 1 else NEXT_PAGE_FLAG_BAIDU
            rel_url = content.xpath('//*[@id="page"]/a[{}]/@href'.format(next_page_index))
            if rel_url:
                self.url = urljoin(self.url, rel_url[0])
            else:
                print("～～～无更多页面数据～～～")
                return

    def search_page(self, url, num, pause=5):
        """
        Baidu search
        :param num: PageNum
        :param url:
        :param pause:
        :return: result
        desc:
                1、百度页面异步js加载，用requests直接获取会丢失页面数据，采用selenium驱动页面
                2、每次请求sleep 5秒，防止百度识别是爬虫请求
        """
        time.sleep(pause)
        driver = webdriver.Chrome(executable_path=DRIVER_PATH, chrome_options=self.get_options())
        try:
            LOGGER.info("正在爬取第{}页....{}".format(num, self.url))
            driver.get(url)
            html = driver.page_source
            selector = etree.HTML(html)
            # print(html)
            # print(selector)
            return selector
        except Exception as e:
            LOGGER.exception(e)
            return None
        finally:
            driver.close()

    def get_options(self):
        # 进入浏览器设置
        options = webdriver.ChromeOptions()
        # 谷歌无头模式
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('window-size=1200x600')
        options.add_argument('--start-maximized')
        # 设置中文
        options.add_argument('lang=zh_CN.UTF-8')

        # 设置代理
        # options.add_argument('--proxy-server=%s' % self.get_random_user_proxy())
        options.add_argument('user-agent=' + self.get_random_user_agent())
        # options.add_argument('--referer=%s' % self.get_random_referer())
        return options

    def get_random_referer(self):
        """
        Get a random referer string.
        :return: Random referer string.
        """
        pass

    def get_random_user_proxy(self):
        """
        Get a random user agent string.
        :return: Random user agent string.
        """
        proxy = random.choice(self.get_data('all_proxy.txt', PROXY))
        return proxy.split("//").pop()

    def get_random_user_agent(self):
        """
        Get a random user agent string.
        :return: Random user agent string.
        """
        return random.choice(self.get_data('user_agents.txt', USER_AGENT))

    def get_random_domain(self):
        """
        Get a random domain.
        :return: Random user agent string.
        """
        domain = random.choice(self.get_data('baidu_domain.txt', DOMAIN_BAIDU))
        if domain in BLACK_DOMAIN_BAIDU:
            self.get_random_domain()
        else:
            return domain

    def get_data(self, filename, default=''):
        """
        Get data from a file
        :param filename: filename
        :param default: default value
        :return: data
        """
        root_folder = os.path.dirname(__file__)
        user_agents_file = os.path.join(os.path.join(root_folder, 'data'), filename)
        try:
            with open(user_agents_file) as fp:
                data = [_.strip() for _ in fp.readlines()]
        except:
            data = [default]
        return data

    def save(self, data):
        with open(self.desc + "_" + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + "_data.csv",
                  'w', newline='', encoding='utf-8-sig') as f:
            for result in data:
                f_csv = csv.writer(f)
                f_csv.writerow(result)


if __name__ == '__main__':
    search = BaiduSpider()
    results = search.search("Python", 3)
    search.save(results)

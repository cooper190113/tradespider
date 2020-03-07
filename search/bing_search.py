import csv
import datetime
import os
import random
import sys
import time

from lxml import etree
from selenium import webdriver

from search.config import LOGGER, USER_AGENT, DRIVER_PATH, REFERE, DOMAIN_BING, BLACK_DOMAIN_BING, URL_SEARCH_BING, \
    PROXY, REFERE_POST_BING, NEXT_PAGE_FLAG_BING

if sys.version_info[0] > 2:
    from urllib.parse import quote_plus, urljoin
else:
    from urllib import quote_plus


#######################
# 问题: 无法获取到每次变动正确的referer
#######################
class BingSpider(object):
    """
        Magic bing search.
    """

    def __init__(self):
        self.desc = "Bing"
        self.url = URL_SEARCH_BING
        self.referer = REFERE.format(DOMAIN_BING)

    def search(self, keywords, num, pause=5):
        """
        Get the results you want,such as title,description,url
        :param keywords:
        :param num: pageNum
        :param pause:
        :return: Generator
        """
        self.url = self.url.format(domain=self.get_random_domain(), query=quote_plus(keywords))

        for i in range(1, int(num) + 1):
            print("正在爬取第{}页....{}".format(i, self.url))

            content = self.search_page(self.url, i, pause)
            results = content.xpath('//*[@id="b_results"]//li')
            for result in results:
                data = []
                title = ""
                title_node = result.xpath("./h2/a//text()") if result.xpath("./h2/a//text()") else None
                if title_node:
                    title = title.join(title_node)
                else:
                    title_node = result.xpath("./div/h2/a//text()") if result.xpath("./div/h2/a//text()") else None
                    title = title if not title_node else title.join(title_node)

                if not title:
                    continue

                url_link = ""
                url_node = result.xpath("./h2/a/@href") if result.xpath("./h2/a/@href") else None
                if url_node:
                    url_link = url_node[0]
                else:
                    url_node = result.xpath("./div/h2/a/@href") if result.xpath("./div/h2/a/@href") else None
                    url_link = url_link if not url_node else url_node[0]

                abstract = ""
                abstract_node = result.xpath('./div[@class="b_caption"]')
                if abstract_node:
                    abstract = abstract_node[0].xpath('string(.)')

                print(title + ", " + url_link + ", " + abstract)
                data.append(title)
                data.append(url_link)
                data.append(abstract)
                yield data

            next_page_index = NEXT_PAGE_FLAG_BING - 1 if i == 1 else NEXT_PAGE_FLAG_BING
            next_page_url = content.xpath(
                '//*[@id="b_results"]/li[@class="b_pag"]/nav/ul/li[{}]/a/@href'.format(next_page_index))
            if next_page_url:
                self.url = urljoin(self.url, next_page_url[0])
            else:
                print("～～～无更多页面数据～～～")
                return

    def search_page(self, url, num, pause=5):
        """
        Bing search
        :param num: pageNum
        :param pause:
        :param url:
        :return: result
        """
        time.sleep(pause)
        driver = webdriver.Chrome(executable_path=DRIVER_PATH, chrome_options=self.get_options(num))
        try:
            LOGGER.info("正在抓取:" + url)
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

    def get_options(self, num):
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

        options.add_argument('--referer=%s' % self.get_random_referer(num))
        return options

    def get_random_referer(self, num):
        """
        Get a random referer string.
        :param num: pageNum
        :return: Random referer string.
        """
        if num == 1:
            referer = REFERE.format(DOMAIN_BING)
        elif num == 2:
            referer = self.url[0:self.url.index("first") - 1]
        else:
            referer = urljoin(self.url, REFERE_POST_BING.format((num - 2) * 10 - 1));
        return referer

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
        domain = random.choice(self.get_data('bing_domain.txt', DOMAIN_BING))
        if domain in BLACK_DOMAIN_BING:
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
    search = BingSpider()
    results = search.search("Python", 5)
    search.save(results)

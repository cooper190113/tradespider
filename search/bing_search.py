import os
import random
import time
import sys

from lxml import etree
from selenium import webdriver

from search.config import LOGGER, USER_AGENT, DRIVER_PATH, REFERE, DOMAIN_BING, BLACK_DOMAIN_BING, URL_SEARCH_BING, \
    PROXY

if sys.version_info[0] > 2:
    from urllib.parse import quote_plus
else:
    from urllib import quote_plus


class BingSpider(object):
    """
        Magic bing search.
    """

    def __init__(self):
        pass

    def search(self, keywords, num=None, pause=5):
        """
        Get the results you want,such as title,description,url
        :param keywords:
        :param num:
        :param pause:
        :return: Generator
        """
        domain = self.get_random_domain()
        url = URL_SEARCH_BING.format(domain=domain, query=quote_plus(keywords))
        content = self.search_page(url, pause)

        yield ["Title", "Url", "Abstract"]
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

    def search_page(self, url, pause=5):
        """
        Google search
        :param pause:
        :param url:
        :return: result
        """
        time.sleep(pause)
        driver = webdriver.Chrome(executable_path=DRIVER_PATH, chrome_options=self.get_options())
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

    def get_options(self, proxy=None, user_agent=None):
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

        options.add_argument('--referer=%s' % REFERE.format(DOMAIN_BING))
        return options

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


if __name__ == '__main__':
    search = BingSpider()
    search.search("Python")

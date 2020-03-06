import json
import time
import urllib.parse
from urllib.parse import urljoin

from lxml import etree
from selenium import webdriver
import csv

# 将Chrome设置置成不加载图片的无界面运行状态
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
chrome_options.add_argument("--headless")
# 可自定义目录，不同浏览器需要选择对应的版本
chrome_path = r'chromedriver.exe'


class BaseSpider(object):
    def parse_page(self):
        pass

    def parse_url(self):
        pass

    def save(self, data):
        pass

    @staticmethod
    def get_page_content(url):
        '''
            1、百度页面异步js加载，用requests直接获取会丢失页面数据，采用selenium驱动页面
            2、每次请求sleep 3秒，防止百度识别是爬虫请求
        :param url:
        :return:
        '''
        time.sleep(3)

        driver = webdriver.Chrome(chrome_path, chrome_options=chrome_options)
        driver.get(url)
        return driver.page_source


class BaiduSpider(BaseSpider):
    def __init__(self, keyword, page_num):
        self.desc = "Baidu"
        self.keyword = str(keyword)
        self.page_num = page_num
        self.url = "https://www.baidu.com/s?" \
                   + urllib.parse.urlencode({'wd': self.keyword}) + "&" + urllib.parse.urlencode({'oq': self.keyword})

    def parse_page(self):

        yield ["Title", "Url", "Abstract"]

        for i in range(1, int(self.page_num) + 1):
            print("正在爬取第{}页....{}".format(i, self.url))
            flag = 11
            html = BaseSpider.get_page_content(self.url)
            content = etree.HTML(html)
            # print(content)
            for j in range(1, flag):
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

            next_page_index = flag - 1 if i == 1 else flag
            rel_url = content.xpath('//*[@id="page"]/a[{}]/@href'.format(next_page_index))
            if rel_url:
                self.url = urljoin(self.url, rel_url[0])
            else:
                print("～～～无更多页面数据～～～")
                return

    def save(self, data):
        with open(self.desc + "_data.csv", 'w', newline='', encoding='utf-8-sig') as f:
            for result in data:
                f_csv = csv.writer(f)
                f_csv.writerow(result)


class BingSpider(BaseSpider):
    def __init__(self, keyword, page_num):
        self.desc = "Bing"
        self.url = ""
        self.keyword = keyword
        self.page_num = page_num

    def parse_page(self):
        pass

    def parse_url(self):
        pass


class GoogleSpider(BaseSpider):
    def __init__(self, keyword, page_num):
        self.desc = "Google"
        self.url = ""
        self.keyword = keyword
        self.page_num = page_num

    def parse_page(self):
        pass

    def parse_url(self):
        pass

from lxml import etree
from selenium import webdriver

# xpath https://www.jianshu.com/p/97a43eb4b2b3
class BingSpider(object):
    def __init__(self, keyword, page_num):
        self.desc = "Google"
        self.url = ""
        self.keyword = keyword
        self.page_num = page_num

    def parse_page(self):
        pass

    def save(self, data):
        pass


proxy = "117.88.4.217:3000"
user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.9 Safari/537.36"

# 进入浏览器设置
options = webdriver.ChromeOptions()
# 谷歌无头模式
# options.add_argument('--headless')
# options.add_argument('--disable-gpu')
# options.add_argument('window-size=1200x600')
options.add_argument('--start-maximized')
# 设置中文
options.add_argument('lang=zh_CN.UTF-8')

# 设置代理
if proxy:
    options.add_argument('--proxy-server=%s' % proxy)
if user_agent:
    options.add_argument('user-agent=' + user_agent)
options.add_argument('--referer=https://cn.bing.com')

driver = webdriver.Chrome(executable_path='../driver/chromedriver.exe', chrome_options=options)

# url = "https://www.baidu.com/s?wd=python"
url = "https://cn.bing.com/search?q=python"
driver.get(url)

html = driver.page_source
if '未连接到互联网' in html:
    print('代理不好使啦')
if 'anti_Spider-checklogin&' in html:
    print('被anti_Spider check啦')
# print(driver.page_source)
# print(driver.current_url)
# print(driver.get_cookies())

selector = etree.HTML(html)

results = selector.xpath('//*[@id="b_results"]//li')
for result in results:
    print(result)
    title = result.xpath("./h2/a//text()") if result.xpath("./h2/a//text()") else None
    if title:
        print(title)
    else:
        title = result.xpath("./div/h2/a//text()") if result.xpath("./div/h2/a//text()") else None
        print(title)
    # for item in items:
    #     a = item.xpath('/h2/a')
    #     print(a[0].xpath('string(.)'))
    # titles = result.xpath('//li/h2/a')
    # if titles:
    #     print(titles[0].xpath('string(.)'))
    # else:
    #     titles = result.xpath('//li/div/h2/a')
    #     print(titles[0].xpath('string(.)'))

# titles = selector.xpath('//*[@id="b_results"]/li/h2/a')
# if titles:
#     print(titles[0].xpath('string(.)'))
# else:
#     titles = selector.xpath('//*[@id="b_results"]/li/div/h2/a')
#     print(titles[0].xpath('string(.)'))


# urls = selector.xpath('//*[@id="b_results"]/li/h2/a/@href')
# abstracts = selector.xpath('//*[@id="b_results"]/li/div/p/text()')
# for title in titles:
#     print(f'{title}')
# print(selector)
# 采集完成关闭浏览器
# driver.close()

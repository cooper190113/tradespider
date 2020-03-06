# from script.baiduparser import BaiduSpider
# from script.bingparser import BingSpider
# from script.googleparser import GoogleSpider
from script.baiduparser import *
from script.bingparser import *
from script.googleparser import *

if __name__ == '__main__':
    search_engine = input("选择搜索引擎[1:Baidu 2:Bing 3:Google]:")
    keyword = input("搜索关键字:")
    page_num = input("搜索页数:")

    while 1:
        if page_num.isdigit():
            break
        else:
            page_num = input("页码错误,请重新输入搜索页数:")

    while 1:
        if not page_num.isdigit():
            search_engine = input("不支持的搜索引擎,请重新选择搜索引擎[1:Baidu 2:Bing 3:Google]:")
            continue

        if int(search_engine) == 1:
            search = BaiduSpider(keyword, page_num)
            break
        elif int(search_engine) == 2:
            search = BingSpider(keyword, page_num)
            break
        elif int(search_engine) == 3:
            search = GoogleSpider(keyword, page_num)
            break
        else:
            search_engine = input("不支持的搜索引擎,请重新选择搜索引擎[1:Baidu 2:Bing 3:Google]:")

    results = search.parse_page()
    search.save(results)

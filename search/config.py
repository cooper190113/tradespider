import logging

# Define some constants
DRIVER_PATH = "../driver/chromedriver.exe"

PROXY = "http://127.0.0.1:1087"

REFERE = "https://{}"

USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.9 Safari/537.36'

BLACK_DOMAIN_GOOGLE = ['www.google.gf', 'www.google.io', 'www.google.com.lc']
DOMAIN_GOOGLE = 'www.google.com'
URL_SEARCH_GOOGLE = "https://{domain}/search?hl={language}&q={query}&btnG=Search&gbv=1"
URL_NUM_GOOGLE = "https://{domain}/search?hl={language}&q={query}&btnG=Search&gbv=1&num={num}"
URL_NEXT_GOOGLE = "https://{domain}/search?hl={language}&q={query}&btnG=Search&gbv=1&num={num}&start={start}"

BLACK_DOMAIN_BAIDU = []
DOMAIN_BAIDU = 'www.baidu.com'
URL_SEARCH_BAIDU = "https://{domain}/s?wq={query}"

BLACK_DOMAIN_BING = []
DOMAIN_BING = 'cn.bing.com'
URL_SEARCH_BING = "https://{domain}/search?q={query}"
REFERE_POST_BING = "{page}&FORM=PERE1"
NEXT_PAGE_FLAG = 7

logging.getLogger("lxml").setLevel(logging.WARNING)
logging.getLogger("selenium").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s: %(message)s')
LOGGER = logging.getLogger('magic_spider')

# -*- coding: utf-8 -*-

# Scrapy settings for doubans project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html


from datetime import datetime

# 文件及路径，log目录需要先建好
# today = datetime.now()
# log_file_path = "../log/scrapy_{}_{}_{}.log".format(today.year, today.month, today.day)
#
# LOG_LEVEL = 'ERROR'
# LOG_FILE = log_file_path

LOG_LEVEL = 'INFO'

EXTENSIONS = {
    'scrapy.extensions.telnet.TelnetConsole': None
 }

CONCURRENT_REQUESTS = 10


BOT_NAME = 'doubans'

SPIDER_MODULES = ['doubans.spiders']
NEWSPIDER_MODULE = 'doubans.spiders'


# MYSQL_HOST = '120.79.185.206'
# MYSQL_DBNAME = 'iRead'
# MYSQL_USER = 'root'
# MYSQL_PASSWD = '1992@Hzj'

MYSQL_HOST = 'localhost'
MYSQL_DBNAME = 'Douban'
MYSQL_USER = 'root'
MYSQL_PASSWD = '12345!@#$%'

DOWNLOAD_DELAY = 1

ITEM_PIPELINES = {
    'doubans.pipelines.DoubansPipeline': 300,
}


# Retry many times since proxies often fail
# 代理模式 0 = Every requests have different proxy
# 这是存放代理IP列表的位置
# Retry on most error codes since proxies fail for different reasons
# RETRY_TIMES = 10
# RETRY_HTTP_CODES = [500, 503, 504, 400, 403, 404, 408]
# DOWNLOADER_MIDDLEWARES = {
#     'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
#     'scrapy_proxies.RandomProxy': 100,
#     'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
# }
# PROXY_LIST = '/Users/suool/PycharmProjects/DouBanSpider/doubans/doubans/url.txt'
# PROXY_MODE = 0

DOWNLOADER_MIDDLEWARES = {
   'doubans.middlewares.RandomUserAgentMiddleware': 543,
   'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
}


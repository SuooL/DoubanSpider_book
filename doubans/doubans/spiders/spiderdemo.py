import scrapy


class TestSpider(scrapy.Spider):
    name = 'test'
    # allowed_domains = ['www.baidu.com']
    start_urls = ['https://book.douban.com/subject/1001103/']

    # 本地爬虫配置文件
    # custom_settings = {
    #     'middlewares': {
    #         'doubans.middlewares.RandomUserAgentMiddleware': 1,
    #     },
    #
    # }

    def parse(self, response):
        print('*_' * 20)
        print(response.status)
        # print(response.headers)
        print('*_' * 20)
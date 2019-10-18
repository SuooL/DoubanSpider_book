# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
import random
import base64
from fake_useragent import UserAgent
import requests
import time


# 代理 ip 提供服务地址
getIPUrl = ''
proxy_ip = ""
expire_time = time.time()
proxy_id = ''
release_count = 0


class RandomUserAgentMiddleware(object):
    '''
    随机更换user-agent
    模仿并替换site-package/scrapy/downloadermiddlewares源代码中的
    useragent.py中的UserAgentMiddleware类
    '''

    def __init__(self, crawler):
        super(RandomUserAgentMiddleware, self).__init__()
        self.ua = UserAgent()
        # 可读取在settings文件中的配置，来决定开源库ua执行的方法，默认是random，也可是ie、Firefox等等
        self.ua_type = crawler.settings.get("RANDOM_UA_TYPE", "random")
        # print(self.ua)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    # 更换用户代理逻辑在此方法中
    def process_request(self, request, spider):
        global expire_time, proxy_ip

        def get_ua():
            return getattr(self.ua, self.ua_type)

        def get_proxy():
            global expire_time, proxy_ip, proxy_id
            req = requests.get(getIPUrl)
            result = req.json()
            if result['ERRORCODE'] == '0':
                proxy_ip = "http://{ip}:{port}".format(ip=result['RESULT']['wanIp'], port=result['RESULT']['proxyport'])
                print("\n获取的IP地址是 %s \n" % proxy_ip)
                expire_time = time.time() + 300
                return proxy_ip
            else:
                time.sleep(15)
                get_proxy()
            # if 'ip' in result['data'][0].keys():
            #     # print(result['data'][0]['ip'], result['data'][0]['http_port'])
            #     with open('url_list.txt', 'a+') as wf:
            #         wf.write(
            #             "http://{ip}:{port}\n".format(ip=result['data'][0]['ip'], port=result['data'][0]['http_port']))
            #     expire_time = result['data'][0]['expire_at_timestamp']
            #     proxy_ip = "http://{ip}:{port}".format(ip=result['data'][0]['ip'], port=result['data'][0]['http_port'])
            #     proxy_id = result['data'][0]['id']
            #     print("\n获取的IP地址是 %s id 是 %s " % (proxy_ip, proxy_id))
            #     return proxy_ip
            # else:
            #     get_proxy()

        def get_release_url():
            global proxy_id, release_count
            release_count += 1
            release_url = 'https://api.2808proxy.com/proxy/release?id={url}&token=ZICG5IPBF2IXHKER2Q3LGGDUOQ8AQ6LC'.\
                format(url=proxy_id)
            req2 = requests.get(release_url)
            result2 = req2.json()
            if result2['status'] == 0:
                print("ip 释放成功, %s" % release_url)
            else:
                print("ip 释放失败 %s " % release_url)
                print(result2['msg'])
                time.sleep(20)
                if release_count > 5:
                    release_count = 0
                    return
                else:
                    get_release_url()

        now = time.time()
        # if float(now) - float(expire_time) > 0:
        #     old_ip = proxy_ip
        #     proxy = get_proxy()
        #     if old_ip == proxy:
        #         proxy = get_proxy()
        #     print("\n当前时间：%.2f, 过期时间 %.2f 时间差是 %d \n" % (now, expire_time, now - expire_time))
        # else:
        #     proxy = proxy_ip
        # request.meta['proxy'] = proxy
        request.headers.setdefault('User-Agent', get_ua())

import csv
#
# file2 = open("url.txt", "w")
#
# with open('ips_pool.csv', 'r') as f:
#     f_csv = csv.reader(f)
#     headers = next(f_csv)
#     for row in f_csv:
#         url = "{}://{}:{}\n".format(row[0].lower(), row[1], row[2])
#         print(url)
#         file2.write(url)
# f.close()
# file2.close()

# 杂七杂八的测试代码

import requests
import time

USERNAME = 'v2exer'
PASSWORD = '4FNkqEA2AShuYni'

getIpUrl = ''

proxy_id = ''


def getUrl():
    global proxy_id
    req = requests.get(getIpUrl)

    result = req.json()
    print(result)
    print(result['ERRORCODE'] == '0')


def realaseUrl():
    global proxy_id
    releaseUrl = 'https://api.2808proxy.com/proxy/release?id={url}&token=ZICG5IPBF2IXHKER2Q3LGGDUOQ8AQ6LC'.format(url=proxy_id)
    req2 = requests.get(releaseUrl)
    result2 = req2.json()
    print(result2['status'])


proxies = {'https': 'http://127.0.0.1:3128'}
resp = requests.get('https://httpbin.org/ip', proxies=proxies)
respj = resp.json()
proxy_ip = 'http://' + respj['origin'].split(',')[0]
print(proxy_ip)

resp = requests.get('https://book.douban.com/subject/1000001/', proxies=proxies)
respj = resp.text


# 第二步：通过代理ip发送请求
# proxy_url_secured = "%s://%s:%s@%s:%d" % ('http', USERNAME, PASSWORD, req['ip'], req['http_port_secured'])
# r = requests.get('http://pv.sohu.com/cityjson', proxies={'http': proxy_url_secured, 'https': proxy_url_secured})
# print("Response with proxy : " + r.text)
# print("sleeping...")
# time.sleep(1)
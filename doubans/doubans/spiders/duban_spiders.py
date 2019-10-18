"""
    scrapy初始Url的两种写法，
    一种是常量start_urls，并且需要定义一个方法parse（）
    另一种是直接定义一个方法：star_requests()
"""

import scrapy
import re
import logging
from doubans.items import BookItem
logger = logging.getLogger(__name__)

# 这里我直接使用 图书 id 遍历爬取，实际上写成 scrapy-redis, 做成分布式更好，这个后面写其他爬虫的时候用上了，这里懒得改先了。

class BookSpider(scrapy.Spider):
    name = "BookSpider"
    allowed_domains = ["books.douban.com"]
    itemCount = 0

    logger.info("开始抓取")
    start_urls = []
    for index in range(10000, 10010):
        book_url = "https://book.douban.com/subject/" + str(1000001+index) + '/'
        start_urls.append(book_url)

    def parse(self, response):
        """
        """
        def get_format_str(params):
            params = params.strip()  # 去掉空格
            params = params.replace(" ", "")
            params = params.replace("\n", "")  # 去掉换行符
            return params

        book = BookItem()
        request_url = response.url
        book_id = re.findall(r'/(\d+)/$', request_url)[0]

        self.itemCount += 1
        if self.itemCount % 100 == 0:
            print("当前已处理 %d 本书" % self.itemCount)

        book['douban_id'] = str(book_id)
        try:
            infos = response.xpath("//div[@id='info']")

            if infos is None or len(infos) == 0:
                logger.error("没有这本编号书 %s\n" % str(book_id))
                with open('exists_list.txt', 'a+') as wf:
                    wf.write("没有这本编号书 %s\n" % str(book_id))
                return

            # 作者相关
            writers = response.xpath("//*[@id='info']/span[a]")

            if len(writers) >= 1:
                book['author'] = ','.join(writers[0].xpath(".//a/text()").extract())[:100]
                if len(writers) == 2:
                    book['translator'] = ','.join(writers[1].xpath(".//a/text()").extract())[:100]
            else:
                if "作者" in infos.extract_first():
                    author = infos.xpath(".//a/text()").extract_first().strip()
                    book['author'] = get_format_str(author)[:100]

            # 次数相关
            read_count = ','.join(response.xpath("//*[@id='collector']/p[a]/a/text()").extract())
            read = re.findall(r'(\d+)人读过', read_count)
            reading = re.findall(r'(\d+)人在读', read_count)
            readw = re.findall(r'(\d+)人想读', read_count)
            if len(read) > 0:
                book['read_count'] = read[0]
            if len(reading) > 0:
                book['reading_count'] = reading[0]
            if len(readw) > 0:
                book['want_count'] = readw[0]

            vote_count = response.xpath("//span[@property='v:votes']/text()").extract_first()
            if vote_count is not None:
                book['rating_count'] = vote_count.strip()
            com_count = response.xpath('//*[@id="content"]/div/div[1]/div[3]/section/header/h2/span/a/text()').extract_first()
            if com_count is not None:
                book['comment_count'] = re.findall(r'\d+', com_count)[0]
            s_com = response.xpath('//div[@class="mod-hd"]/h2/span')
            if len(s_com) == 2:
                com_full = s_com[1].xpath('.//a/text()').extract_first()
                book['scom_count'] = re.findall(r'\d+', com_full)[0]

            # 简介相关
            intro = response.xpath('//div[@class="intro"]')
            if len(intro) == 1:
                book['summary'] = ''.join(intro[0].xpath('.//p/text()').extract())[:5980]
            if len(intro) == 2:
                book['summary'] = ''.join(intro[0].xpath('.//p/text()').extract())[:5980]
                book['author_intro'] = ''.join(intro[1].xpath('.//p/text()').extract())[:3980]
            if len(intro) == 4:
                book['summary'] = ''.join(intro[1].xpath('.//p/text()').extract())[:5980]
                book['author_intro'] = ''.join(intro[3].xpath('.//p/text()').extract())[:3980]
            if len(intro) == 3:
                book['author_intro'] = ''.join(intro[2].xpath('.//p/text()').extract())[:3980]
                summary_int = ''.join(intro[1].xpath('.//p/text()').extract())
                count = re.findall(r'\.\.\.$', summary_int)
                if len(count) == 0:
                    book['summary'] = ''.join(intro[0].xpath('.//p/text()').extract())[:5980]
                else:
                    book['summary'] = ''.join(intro[1].xpath('.//p/text()').extract())[:5980]

            # 目录
            toc = response.xpath('//*[@id="dir_{value}_full"]/text()'.format(value=book_id)).extract()
            if toc is not None:
                del toc[-2:]
                for index in range(len(toc)):
                    toc[index] = toc[index].replace("\n", "").strip()
                book['toc'] = '\n'.join(toc)[:5980]
            else:
                pass

            # 基本信息
            img_url = response.xpath("//div[@id='mainpic']/a[@class='nbg']/@href").extract_first()
            name = response.xpath("//span[@property='v:itemreviewed']/text()").extract_first()
            score = response.xpath("//strong[@property='v:average']/text()").extract_first().strip()
            label = response.xpath("//a[@class='  tag']/text()").extract()

            book['title'] = name
            book['detail_url'] = response.url
            book['label'] = ",".join(label)
            book['rating'] = score
            book['images'] = img_url
            link_t = response.xpath("//*[@id='info']/a/text()").extract()

            logger.info("编号 %s 书名《%s》" % (str(book_id), str(name)))

            cur_type = ""  # 当前获取的类型
            # print(infos.xpath("./*"))
            # print(infos.xpath("./text()"))
            # if "作者" in infos.extract_first():
            #     author = infos.xpath(".//a/text()").extract_first().strip()
            #     book['author'] = self.getFormatStr(author)

            # print("作者：", infos.xpath(".//a/text()").extract_first().strip())
            info_list = infos.xpath("./*|./text()")
            for index in range(len(info_list)):
                info = info_list[index]
            # for info in infos.xpath("./*|./text()"):
                name = info.xpath("text()").extract_first()
                if name is not None:
                    cur_type = ""
                # if "作者:" == name or "作者" == name:
                #     cur_type = "author"
                #     continue
                if "出版社:" == name:
                    cur_type = "publisher"
                    continue
                elif "出版年:" == name:
                    cur_type = "pubdate"
                    continue
                elif "页数:" == name:
                    cur_type = "pages"
                    continue
                elif "定价:" == name:
                    cur_type = "price"
                    continue
                elif "ISBN:" == name:
                    cur_type = "isbn"
                    continue
                elif "装帧:" == name:
                    cur_type = "binding"
                    continue
                elif "出品方:" == name:
                    cur_type = "producer"
                    book['producer'] = link_t[0]
                    continue
                elif "副标题:" == name:
                    cur_type = "subtitle"
                    continue
                elif "原作名:" == name:
                    cur_type = "origin_title"
                    continue
                elif "丛书:" == name:
                    cur_type = "series"
                    book['series'] = link_t[-1]
                    continue

                span = info.extract()
                span = span.strip()  # 去掉空格
                span = span.replace("\n", "")  # 去掉换行符
                span = span.replace("<br>", "")  # 去掉换行符
                if len(span) != 0:
                    # if cur_type == "author":
                    # book['author'] = self.getFormatStr(info.xpath("text()").extract_first())  # 作者名字特殊一点
                    if cur_type == "publisher":
                        book['publisher'] = span
                    elif cur_type == "pubdate":
                        book['pubdate'] = span
                    elif cur_type == "pages":
                        page = re.sub(r"\D", "", span)

                        book['pages'] = page if len(page) != 0 else 0  # todo 这里限制只获取数字 去掉冒号 单位
                    elif cur_type == "price":
                        book['price'] = float(re.findall(r"\d+\.?\d*", span)[0])
                    elif cur_type == "isbn":
                        book['isbn'] = span
                    elif cur_type == "binding":
                        book['binding'] = span

                    elif cur_type == "subtitle":
                        book['subtitle'] = span[:100]
                    elif cur_type == "origin_title":
                        book['origin_title'] = span[:100]
                    elif cur_type == "translator":
                        book['translator'] = span
                    elif cur_type == "series":
                        book['series'] = span
            yield book

        except Exception as e:
            logger.error("%s 号书出错" % str(book_id))
            print("%s 号书出错" % str(book_id))
            print(e)
            with open('wrong_list.txt', 'a+') as wf:
                wf.write("%s\n" % str(book_id))

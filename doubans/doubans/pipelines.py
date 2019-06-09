# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from doubans import settings
from pymysql import connections
import logging
logger = logging.getLogger(__name__)

class DoubansPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True)
        self.place_holder = ""
        self.select_key = ""
        self.params = []
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        self.place_holder = ""
        self.select_key = ""
        self.params = []

        sql = "insert into Book_Info("

        for key, values in item.items():
            if self.select_key != "":
                self.select_key += ","
            self.select_key += key
            if self.place_holder != "":
                self.place_holder += ","
            self.place_holder += "%s"
            self.params.append(values)

        sql += self.select_key + ") VALUES(" + self.place_holder + ")"

        try:
            self.cursor.execute(sql, self.params)
            self.connect.commit()
        except Exception as e:
            logger.error("%s 号书存储出错" % item['douban_id'])
            print("%s 号书存储出错" % item['douban_id'])
            with open('save_list.txt', 'a+') as wf:
                wf.write("%s\n" % item['douban_id'])
            pass
        return item

    def close_spider(self, spider):
        self.connect.close()



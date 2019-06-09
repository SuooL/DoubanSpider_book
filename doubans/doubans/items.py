# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class BookItem(Item):

    douban_id = Field()
    title = Field()
    origin_title = Field()
    subtitle = Field()
    author = Field()
    producer = Field()
    translator = Field()
    price = Field()
    isbn = Field()
    publisher = Field()
    pubdate = Field()
    pages = Field()
    binding = Field()
    images = Field()
    toc = Field()
    rating = Field()
    rating_count = Field()
    summary = Field()
    author_intro = Field()
    label = Field()
    detail_url = Field()
    comment_count = Field()
    scom_count = Field()
    read_count = Field()
    want_count = Field()
    reading_count = Field()
    series = Field()

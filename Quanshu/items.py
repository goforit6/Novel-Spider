# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QuanshuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    typeof = scrapy.Field()
    novel_title = scrapy.Field()
    author = scrapy.Field()
    chapter_name = scrapy.Field()
    chapter_content = scrapy.Field()

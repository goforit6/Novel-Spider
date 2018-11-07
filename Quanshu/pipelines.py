# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo


class QuanshuPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db, mongo_set):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.mongo_set = mongo_set

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB'),
            mongo_set=crawler.settings.get('MONGO_SET')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.collections = self.db[self.mongo_set]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.collections.update({'chapter_name': item['chapter_name']}, dict(item), True)
        return item

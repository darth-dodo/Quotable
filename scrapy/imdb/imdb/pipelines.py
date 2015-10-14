# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


# class ImdbPipeline(object):
#     def process_item(self, item, spider):
#         return item


import pymongo
import re
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log
import pprint


class ImdbPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        self.db = connection[settings['MONGODB_DB']]
        # self.collection = self.db['imdb_top250']
        self.collection = self.db['imdb_top250tv']
        # self.collection = self.db['raj']

    def process_item(self, item, spider):
        self.collection.update(
                               {'name':item['name']}
                               ,dict(item)
                               ,upsert = True)

        log.msg("Quote added to MongoDB !", level=log.DEBUG, spider=spider)

        return item



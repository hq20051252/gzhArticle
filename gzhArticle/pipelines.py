# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import json

from scrapy import log
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from gzhArticle.settings import DATAHOME


class MongoDBPipeline(object):
    def __init__(self):
        self.server = settings['MONGODB_SERVER']
        self.port = settings['MONGODB_PORT']
        self.db = settings['MONGODB_DB']
        self.col = settings['MONGODB_COLLECTION']
        connection = pymongo.Connection(host=self.server, port=self.port)
        db = connection[self.db]
        self.collection = db[self.col]

    def process_item(self, item, spider):
        err_msg = ''
        if item['content_url'] == '':
            err_msg += 'Missing article %s from site %s by user %s.\n' % (item['title'], item['content_url'], item['serid'])
        if err_msg:
            raise DropItem(err_msg)
        self.collection.insert(dict(item))
        log.msg('Item written to MongoDB database %s/%s' % (self.db, self.col),
                level=log.DEBUG, spider=spider)
        return item


class JsonPipeline(object):

    def __init__(self):
        self.file = open(DATAHOME + '/article.j1', 'wb')

    def process_item(self, item, spider):
        try:
            line = json.dumps(dict(item)) + "\n"
            self.file.write(line)
        except Exception, e:
            log.err(e.message)

        return item
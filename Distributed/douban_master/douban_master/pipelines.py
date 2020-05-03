# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import redis

class DoubanMasterPipeline(object):

    def __init__(self):
        # 初始化redis连接参数
        self.REDIS_HOST = '127.0.0.1'
        self.REDIS_PORT = '6379'
        self.r = redis.Redis(host=self.REDIS_HOST, port=self.REDIS_PORT)

    def process_item(self, item, spider):
        # 向数据库中插入urls
        self.r.lpush('douban:start_urls', item['url'])
        return item
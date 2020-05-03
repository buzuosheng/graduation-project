# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
import pymysql
import pymysql.cursors
import importlib,sys 
importlib.reload(sys)
from scrapy.exporters import JsonItemExporter
from douban_slaver.items import db_slaverItem
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
# from datetime import datetime

class jsonPipeline(object):
    def __init__(self):
        # 打开文件，二进制写入
        self.file = open('doubanTv.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding="utf-8", ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

# 爬虫
# class InfoPipeline(object):

#     def process_item(self, item, spider):
#         #utcnow() 是获取UTC时间
#         item["crawled"] = datetime.utcnow()
#         # 爬虫名
#         item["spider"] = spider.name
#         return item

# 下载图片
class GetImagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for image_url in item['tv_img']:
            yield scrapy.Request(image_url, meta={ 'item': item })

    def file_path(self, request, response=None, info=None):
        # 图片名与网页中的一致
        url = request.url
        file_name = url.split('/')[-1]

        # 使用剧名命名
        # item = request.meta['item']
        # title = item['title']
        # url = request.url
        # file_name = title + '.' + url.split('.')[-1]
        return file_name

    def item_completed(self, results, item, info):
        # 将下载的图片路径（传入到results中）存储到 image_paths 项目组中，如果其中没有图片，我们将丢弃项目:
        tv_img_path = [x['path'] for ok, x in results if ok]
        if not tv_img_path:
            raise DropItem("Item contains no images")
        item['tv_img_path'] = tv_img_path
        return item

# 存储到数据库中
class SavePipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(user="root", db="douban_tv", password="w123456",
                                    host="localhost", charset="utf8", use_unicode=True)

        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
            insert into tv_tb(title, alias, url, tv_img, director, actors, tv_type, c_or_r, first_time, series, single, rate, votes_num, synopsis)
            value(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        self.cursor.execute(insert_sql, (item["title"], item["alias"], item["url"], item["tv_img"],
                                item["director"], item["actors"], item["tv_type"],
                                item["country_or_region"], item["first_time"], item["series"],
                                item["single"], item["rate"], item["votes_num"], item["synopsis"]))

        self.conn.commit()
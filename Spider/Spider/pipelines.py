# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import pymysql.cursors
import importlib,sys
importlib.reload(sys)
from scrapy.exporters import JsonItemExporter
from Spider.items import TvListItem
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
# 导入输出图片工具
from pyecharts.render import make_snapshot
# 使用snapshot-selenium 渲染图片
from snapshot_selenium import snapshot
import pyecharts.options as opts
from pyecharts.charts import Line
from numpy import arange
import csv

# 保存为JSON文件
class tvSpiderPipeline(object):
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

# 写入CSV文件
class CSVPipelime(object):
    def open_spider(self,spider):
        self.file = open("tv.csv",'w',encoding="utf-8", newline='')
        self.writer = csv.writer(self.file)

    def process_item(self, item, spider):
        data = [item["title"], item["alias"], item["url"], ''.join(item["tv_img"]),
                item["director"], item["actors"], item["tv_type"],
                item["country_or_region"], item["first_time"], item["series"],
                item["single"], item["rate"], item["votes_num"], item["synopsis"]]
        self.writer.writerow(data)
        return data

    def close_spider(self,spider):
        self.file.close()

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
class SaveDBPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(user="root", db="tv", password="w123456",
                                    host="localhost", charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
            insert into test(title, alias, url, tv_img, director, actors, tv_type, c_or_r, first_time, series, single, rate, votes_num, synopsis)
            value(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        self.cursor.execute(insert_sql, (item["title"], item["alias"], item["url"], item["tv_img"],
                                item["director"], item["actors"], item["tv_type"],
                                item["country_or_region"], item["first_time"], item["series"],
                                item["single"], item["rate"], item["votes_num"], item["synopsis"]))

        self.conn.commit()

# 如果发现重复的就抛弃item
class DuplicatesPipeline(object):
    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['title'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['title'])
            return item

# 生成折线图
class ZhexianPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(user="root", db="tv", password="w123456",
                                    host="localhost", charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        cur = self.cursor
        select_sql = "select rate from test"
        cur.execute(select_sql)
        ret = cur.fetchall()
        #print(ret)

        xli = []
        yli = [0]*100

        for i in arange(1, 101):
            xli.append(str(float(i)/10))
        for j in ret:
            yli[int(float(j[0])*10)] += 1

        #print(xli)
        #print(yli)

        l = (
            Line()
            .add_xaxis(xli)            #x轴坐标点必须是string类型
            .add_yaxis("电视剧部数", yli, is_smooth=True)
            .set_global_opts(title_opts=opts.TitleOpts(title="电视剧评分分布图"))
        )

        # 输出保存为图片
        make_snapshot(snapshot, l.render("actor.html"), "D:\\Design\\Spider\\actor.png")
        # 保存路径可以自定义，输入图片文件的速度较慢 ，可以先输出网页，测试成功后，再转成图片
        print("已生成图片")

        cur.close() # 关闭游标
        self.conn.close() # 关闭连接

# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy
from scrapy.item import Item, Field

class TvListItem(Item):
    # 电视剧名和年份
    title = scrapy.Field()

    # 又名
    alias = scrapy.Field()

    # 宣传图片
    tv_img = scrapy.Field()
    tv_img_path = scrapy.Field()

    # 电视剧链接
    url = scrapy.Field()

    # 导演
    director = scrapy.Field()

    # 主演
    actors = scrapy.Field()

    # 电视剧类型
    tv_type = scrapy.Field()

    # 制片国家或地区
    country_or_region = scrapy.Field()

    # 首播时间
    first_time = scrapy.Field()

    # 集数
    series = scrapy.Field()

    # 单集时长
    single = scrapy.Field()

    # 豆瓣评分
    rate = scrapy.Field()

    # 评分人数
    votes_num = scrapy.Field()

    # 剧情简介
    synopsis = scrapy.Field()
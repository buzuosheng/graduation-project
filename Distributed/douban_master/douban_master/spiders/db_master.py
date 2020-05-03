import scrapy
from douban_master.items import db_masterItem
import json


class db_master(scrapy.Spider):
    name = 'db_master'
    allow_domain = ["movie.douban.com"]

    def __init__(self, *args, **kwargs):
        super(db_master, self).__init__(*args, **kwargs)
        self.start_urls = ["https://movie.douban.com/j/search_subjects?type=tv&tag=热门&sort=recommend&page_limit=20&page_start=0"]


    def parse(self, response):
        results = json.loads(response.body)['subjects']
        for result in results:
            item = db_masterItem()
            url = result['url']

            item['url'] = url.strip()
            # print(url)
            yield item
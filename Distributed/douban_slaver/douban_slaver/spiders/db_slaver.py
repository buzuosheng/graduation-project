import scrapy
from scrapy.selector import Selector
from douban_slaver.items import db_slaverItem
import scrapy_redis
from scrapy_redis.spiders import RedisSpider

# 开始地址 https://movie.douban.com/tv/#!type=tv&tag=热门&sort=time&page_limit=20&page_start=0

class tvSpider(RedisSpider):
    name = "db_slaver"
    redis_key = 'douban:start_urls'
    # allowed_domain = ["movie.douban.com"]

    # def __init__(self, *args, **kwargs):
    #     super(tvSpider, self).__init__(*args, **kwargs)
    #     # + str(x) for x in range(0, 60 ,20)
    #     self.start_urls = ["https://movie.douban.com/j/search_subjects?type=tv&tag=热门&sort=recommend&page_limit=20&page_start=0"]

    # 动态获取域范围
    def __init__(self, *args, **kwargs):
         domain = kwargs.pop('domain', '')
         self.allowed_domains = filter(None, domain.split(','))
         super(tvSpider, self).__init__(*args, **kwargs)

    # def parse(self, response):
    #     results = json.loads(response.body)['subjects']
    #     for result in results:
    #         tv_item = db_slaverItem()
    #         url = result['url']

    #         tv_item['url'] = url.strip()
    #         # print(url)

    #         yield scrapy.Request(url=url, meta={'tv_item': tv_item}, callback=self.parse_detail)

    def parse(self, response):
        # tv_item = response.meta['tv_item']
        tv_item = db_slaverItem()
        result = Selector(response)

        # 字符串前加u表示处理中文字符

        tv_url = result.xpath('//a[@class="nbgnbg"]/@href').extract()[0]
        url = tv_url.split('photo')[0]

        # 剧名
        title = result.xpath(u'//div[@id="content"]/h1/span[1]/text()').extract()[0] + result.xpath('//div[@id="content"]/h1/span[2]/text()').extract()[0]

        # 又名
        has_alias = result.xpath(u'//div[@id="info"]//span[text()="又名:"]').extract()
        if has_alias:
            alias = result.xpath(u'//div[@id="info"]//span[text()="又名:"]/following::text()[1]').extract()[0]
        else:
            alias = ''

        # 图片
        tv_img = result.xpath('//a[@class="nbgnbg"]/img/@src').extract()[0]

        # 导演
        has_dir = result.xpath('//div[@id="content"]//span[text()="导演"]')
        if has_dir:
            directors = result.xpath('//div[@id="info"]//span[@class="attrs"]//a[@rel="v:directedBy"]/text()')
            director_lsit = directors[:3].extract()
            director = '/'.join(director_lsit)
        else:
            director = ''

        # 主演
        all_actors = result.xpath('//div[@id="info"]//span[@class="attrs"]//a[@rel="v:starring"]/text()')
        actors_list = all_actors[:5].extract()
        actors = '/'.join(actors_list)

        # 类型
        tv_types = result.xpath('//div[@id="info"]//span[@property="v:genre"]/text()')
        type_list = tv_types.extract()
        tv_type = '/'.join(type_list)

        # 制片地区或国家
        country_or_region = result.xpath(u'//div[@id="info"]//span[text()="制片国家/地区:"]/following::text()[1]').extract()[0]

        # 首播
        first_time = result.xpath('//div[@id="content"]//span[@property="v:initialReleaseDate"]/text()').extract()[0]

        # 集数 
        series = result.xpath(u'//div[@id="content"]//span[text()="集数:"]/following::text()[1]').extract()[0]

        # 单集
        has_single = result.xpath('//div[@id="content"]//span[text()="单集片长:"]')
        if has_single:
            single = result.xpath(u'//div[@id="content"]//span[text()="单集片长:"]/following::text()[1]').extract()[0]
        else:
            single = ''

        # 评分
        rate = result.xpath('//strong/text()').extract()[0]

        # 评分人数
        votes_num = result.xpath('//span[@property="v:votes"]/text()').extract()[0]

        # 简介
        has_synopsis = result.xpath('//span[@property="v:summary"]')
        if has_synopsis:
            synopsis = result.xpath('//span[@property="v:summary"]/text()').extract()[0].strip()
        else:
            synopsis = ''

        tv_item['url'] = url.strip()
        tv_item['title'] = title.strip()
        tv_item['alias'] = alias.strip()
        tv_item['tv_img'] = [tv_img.strip()]
        tv_item['director'] = director.strip()
        tv_item['actors'] = actors.strip()
        tv_item['tv_type'] = tv_type.strip()
        tv_item['country_or_region'] = country_or_region.strip() 
        tv_item['first_time'] = first_time.strip()
        tv_item['series'] = series.strip()
        tv_item['single'] = single.strip()
        tv_item['rate'] = rate.strip()
        tv_item['votes_num'] = votes_num.strip()
        tv_item['synopsis'] = synopsis[0:50]

        yield tv_item

        # print('电视剧信息>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
        # print('剧名：' + title)
        # print('又名：' + alias)
        # print('海报：' + tv_img)
        # print('导演：' + director)    
        # print('主演：' + actors)       
        # print('类型：' + tv_type)     
        # print('制片国家或地区：' + country_or_region)
        # print('首播：' + first_time)
        # print('集数：' + series)
        # print('单集时长：' + single)
        # print('评分：' + rate)
        # print('评分人数：' + votes_num)
        # print('简介：' + synopsis)
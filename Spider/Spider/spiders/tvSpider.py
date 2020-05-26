import scrapy
from scrapy.selector import Selector
from Spider.items import TvListItem
import json

# 开始地址 https://movie.douban.com/tv/#!type=tv&tag=热门&sort=time&page_limit=20&page_start=0
# 标签 热门 美剧 英剧 韩剧 日剧 国产剧 港剧 日本动画 综艺 纪录片
class tvSpider(scrapy.Spider):
    name = "douban_tv"
    allowed_domain = ["movie.douban.com"]

    def __init__(self, *args, **kwargs):
        super(tvSpider, self).__init__(*args, **kwargs)
        # + str(x) for x in range(0, 60 ,20)
        self.start_urls = ["https://movie.douban.com/j/search_subjects?type=tv&tag=热门&sort=recommend&page_limit=20&page_start=" + str(x) for x in range(0, 100 ,20)]

    def parse(self, response):
        results = json.loads(response.body)['subjects']
        for result in results:
            tv_item = TvListItem()
            url = result['url']

            tv_item['url'] = url.strip()
            # print(url)

            yield scrapy.Request(url=url, meta={'tv_item': tv_item}, callback=self.parse_detail)

    def parse_detail(self, response):
        tv_item = response.meta['tv_item']
        result = Selector(response)

        # 字符串前加u表示处理中文字符

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
        has_actor = result.xpath('//div[@id="info"]//span[@class="attrs"]//a[@rel="v:starring"]')
        if has_actor:
            all_actors = result.xpath('//div[@id="info"]//span[@class="attrs"]//a[@rel="v:starring"]/text()')
            actors_list = all_actors[:5].extract()
            actors = '/'.join(actors_list)
        else:
            actors = ''

        # 类型
        has_type = result.xpath('//div[@id="info"]//span[@property="v:genre"]')
        if has_type:
            tv_types = result.xpath('//div[@id="info"]//span[@property="v:genre"]/text()')
            type_list = tv_types.extract()
            tv_type = '/'.join(type_list)
        else:
            tv_type = ''

        # 制片地区或国家
        country_or_region = result.xpath(u'//div[@id="info"]//span[text()="制片国家/地区:"]/following::text()[1]').extract()[0]

        # 首播
        has_first_time = result.xpath('//div[@id="content"]//span[@property="v:initialReleaseDate"]')
        if has_first_time:
            first_time = result.xpath('//div[@id="content"]//span[@property="v:initialReleaseDate"]/text()').extract()[0]
        else:
            first_time = ''

        # 集数
        has_series = series = result.xpath(u'//div[@id="content"]//span[text()="集数:"]')
        if has_series:
            series = result.xpath(u'//div[@id="content"]//span[text()="集数:"]/following::text()[1]').extract()[0]
        else:
            series = ''

        # 单集
        has_single = result.xpath('//div[@id="content"]//span[text()="单集片长:"]')
        if has_single:
            single = result.xpath(u'//div[@id="content"]//span[text()="单集片长:"]/following::text()[1]').extract()[0]
        else:
            single = ''

        # 评分
        has_rate = result.xpath('//strong')
        if has_rate:
            rate = result.xpath('//strong/text()').extract()[0]
        else:
            rate = ''

        # 评分人数
        has_vote = result.xpath('//span[@property="v:votes"]')
        if has_vote:
            votes_num = result.xpath('//span[@property="v:votes"]/text()').extract()[0]
        else:
            votes_num = ''

        # 简介
        has_synopsis = result.xpath('//span[@property="v:summary"]')
        if has_synopsis:
            synopsis = result.xpath('//span[@property="v:summary"]/text()').extract()[0].strip()
        else:
            synopsis = ''

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

        # 将tv_item压入到
        yield tv_item

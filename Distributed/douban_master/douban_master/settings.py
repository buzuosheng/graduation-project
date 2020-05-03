# -*- coding: utf-8 -*-

BOT_NAME = 'douban_master'

SPIDER_MODULES = ['douban_master.spiders']
NEWSPIDER_MODULE = 'douban_master.spiders'

# Override the default request headers: 默认请求头
DEFAULT_REQUEST_HEADERS = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Accept-Language': 'en',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
}

# Configure item pipelines 配置item管道文件
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'douban_master.pipelines.DoubanMasterPipeline': 300,
}

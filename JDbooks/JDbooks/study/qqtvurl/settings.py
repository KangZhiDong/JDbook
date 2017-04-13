# -*- coding: utf-8 -*-

# Scrapy settings for qqtvurl project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'qqtvurl'

SPIDER_MODULES = ['qqtvurl.spiders']
NEWSPIDER_MODULE = 'qqtvurl.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'qqtvurl (+http://www.yourdomain.com)'

ITEM_PIPELINES = ['qqtvurl.pipelines.QqtvurlPipeline']

SCHEDULER = "scrapy_redis.scheduler.Scheduler"
SCHEDULER_PERSIST = True
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderPriorityQueue'
REDIS_URL = None
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379

MONGODB_HOST = '127.0.0.1'
MONGODB_PORT = 27017
MONGODB_DBNAME = 'Jikexueyuan'
MONGODB_DOCNAME = 'qqtv2'
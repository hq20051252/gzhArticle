# -*- coding: utf-8 -*-

# Scrapy settings for gzhArticle project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'gzhArticle'

SPIDER_MODULES = ['gzhArticle.spiders']
NEWSPIDER_MODULE = 'gzhArticle.spiders'

#DOWNLOADER_MIDDLEWARES = {
#    }

ITEM_PIPELINES = {'gzhArticle.pipelines.MongoDBPipeline':200}
#ITEM_PIPELINES = {'gzhArticle.pipelines.JsonPipeline':200}

CONCURRENT_REQUESTS = 1

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Linux; U; Android 4.4.2; zh-cn; MX4 Build/KOT49H) AppleWebKit/533.1 (KHTML, like Gecko)Version/4.0 MQQBrowser/5.5 Mobile Safari/533.1 MicroMessenger/6.0.0.58_r884092.501 NetType/WIFI'

# 用户id
BIZ_FILE = "/home/hadoop/workspace/work/gzhArticle/data/users.j1"
DATAHOME = "/home/hadoop/workspace/work/gzhArticle/data/"

# 延时
DOWNLOAD_DELAY = 1
RANDOMIZE_DOWNLOAD_DELAY = True

# 取消cookie
COOKIES_ENABLED = False

# 日志
LOG_LEVEL = "DEBUG"
LOG_FILE = "/home/hadoop/workspace/work/gzhArticle/logs/scrapy.log"

# 数据库
MONGODB_SERVER = "172.16.100.151"
MONGODB_PORT = 27017
MONGODB_DB = "weixin"
MONGODB_COLLECTION = "article"
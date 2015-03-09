# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GzhArticleItem(scrapy.Item):
    # 公众帐号
    userid = scrapy.Field()
    # 公众帐号加密版
    serid = scrapy.Field()
    # 用户名
    author = scrapy.Field()
    # 文章标题
    title = scrapy.Field()
    # 文章封面
    cover = scrapy.Field()
    # 文章摘要
    digest = scrapy.Field()
    # 文章编号
    fileid = scrapy.Field()
    # 发表时间
    datetime = scrapy.Field()
    # 文章链接
    content_url = scrapy.Field()
    # 文章内容
    #content = scrapy.Field()
    # 文章期号
    mid = scrapy.Field()
    # 文章当期编号
    idx = scrapy.Field()
    # N\A
    sn  = scrapy.Field()
    # N\A
    source_url = scrapy.Field()


#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import re
import time
import json
import scrapy
import urllib
import urllib2
import urlparse

from scrapy import log
from scrapy import Request
from gzhArticle.items import GzhArticleItem
from gzhArticle.settings import BIZ_FILE

def sendmsg():
    os.system("ssh hadoop@172.16.100.150 \"bash /home/hadoop/contact_by_sms.sh\"")

class ReadnumcrawlerSpider(scrapy.Spider):
    name = "readnumCrawler"
    allowed_domains = ["mp.weixin.qq.com"]
    start_urls = (
        'http://mp.weixin.qq.com/mp/getmasssendmsg?',
    )

    # 分析 json 字符串. 如果errmsg 为 "no session" 表示key 过期,
    # 返回一个request对象, 重新请求页面.
    def _parse_json(self, mm_j):
        # TODO
        return

    # 从url 中更新 key 参数.
    def reloadkey(self, url, key):
        try:
            baseurl, query = urllib.splitquery(url)
            if query:
                _query = urlparse.parse_qs(query)
                _query.pop('key')
                _query.pop('uin')
                _query.pop('pass_ticket')
                _query.pop('version')
                _query.pop('devicetype')
                _query['key'] = key['key']
                _query['uin'] = key['uin']
                _query['version'] = key['version']
                _query['devicetype'] = key['devicetype']
                _query['pass_ticket'] = key['pass_ticket']
                query = urllib.urlencode(_query)
                return baseurl + "?" + query
            return None
        except ValueError, e:
            log.msg(e.message, level = log.ERROR)
            return None
        except TypeError, e:
            log.msg(e.message, level = log.ERROR)
            return None

    def parse(self, response):
        article_list = []
        log.msg("Response Body is :\n %s." % response.body, level=log.DEBUG)
        a_list = response.body

        try:
            mm_j = json.loads(a_list)
        except ValueError, e:
            comment = u"您的版本不支持此功能，请升级。"
            start = a_list.find(comment)
            if start > 0:
                mm_j = {}
            else:
                log.msg("Cant decode the message, %s." %a_list, level = log.ERROR)
                return article_list


        # mm_j为{} , 就说明 key 失效, 返回,重新请求页面.
        if not mm_j.has_key("ret"):
            self.key = self.__getkeys__()
            url = self.reloadkey(response.url, self.key)
            if not url:
                return None

            return Request(url)

        elif mm_j['ret'] == 0:
            # errmsg 等于 ok , 说明 key 有效, 解析出文章来.
            log.msg(repr(mm_j), level = log.DEBUG)
            article_list = self._parse_json(mm_j)
            log.msg("Now scrapy %s articles." %len(article_list), level = log.INFO)
            log.msg(a_list, level = log.INFO)

            return article_list

        elif mm_j['ret'] == -3:
            self.key = self.__getkeys__()
            url = self.reloadkey(response.url, self.key)
            if not url:
                return None

            return Request(url)

        else:
            log.msg("The wrong reponse CDATA[[%s]], and the url is CDATA[[%s]]." % (repr(mm_j), response.url), level=log.DEBUG)
            return []


    # 从接口中取得key.
    def __getkeys__(self):
        KEY_SERVICE = r"http://172.16.18.154:8180/getkey"
        #KEY_SERVICE = r"http://60.247.57.205:8180/getkey"

        sendmsg()
        time.sleep(6)
        key = {}
        start = time.time()
        while not key:
            log.msg("There is no valid key, try again after 1 second." , level = log.INFO)

            time.sleep(6)
            end = time.time()
            costed  = end - start

            # 遇到整点时,短信提醒.提醒后,休息1秒, 避开整点.
            if int(costed % 60*60) > 0 and int(costed % 60*60) < 8:
                sendmsg()
                time.sleep(1)

            try:
                data = urllib2.urlopen(KEY_SERVICE).read()
                log.msg(data, level = log.DEBUG)
                key = json.loads(data)
            except urllib2.URLError, e:
                log.msg(e.message, level = log.ERROR)
            except urllib2.HTTPError, e:
                log.msg(e.message, level = log.ERROR)
            except ValueError, e:
                log.msg(e.message, level = log.ERROR)

        return key

    def start_requests(self):
        self.key = {}
        interface =  self.start_urls[0]
        biz_file = BIZ_FILE
        fd = open(biz_file, 'rb')

        progress = 0
        for line in fd.xreadlines():

            # 向接口请求一个有效的key. __getkeys__()会不停的循环, 直到取到有效的key, 并返回.
            if not self.key:
                log.msg("There is no valid key. Wait for getting valid key.", level = log.INFO)
                self.key = self.__getkeys__()
                log.msg("Reload key successfully.Now uin: %s, key:%s." %(self.key.get('uin'), self.key.get('key')), level = log.INFO)
                #log.msg("The key is :%s." %repr(self.key), level = log.DEBUG)

            key = self.key['key']
            uin = self.key['uin']
            version = self.key['version']
            devicetype = self.key['devicetype']
            pass_ticket = self.key['pass_ticket']

            # f指定返回的格式,count指定返回的数量.
            f = "json"
            count = 100


            # 获取公众号的serid, 加密后的id.拿不到就跳过这一行.
            try:
                user = json.loads(line)
                __biz = user.get('serid',"")

                if not __biz:
                    continue
                elif len(__biz) > 50:
                    continue
                else:
                    pass
            except ValueError, e:
                log.msg("This is a invalid json serielizer json object. \n %" %line, level = log.INFO)
                continue



            # 构造请求, 使用迭代器的形式逐个返回request对象.
            options = [("__biz", __biz), ('uin', uin), ('key', key), ("f", f), ("count", count), ("version", version), ("devicetype", devicetype), ("pass_ticket", pass_ticket)]
            encoded_opt = urllib.urlencode(options)
            url = interface + encoded_opt
            progress += 1
            log.msg("Get the %s user's page." %progress, level = log.INFO)
            yield self.make_requests_from_url(url)

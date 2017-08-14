# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb
import logging
from scrapy import log
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class DangdangpcPipeline(object):

    def __init__(self):
        conn = MySQLdb.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            passwd='panli',
            db='db_dangdang_re',
            charset='utf8'
        )
        self.conn = conn

    def process_item(self, item, spider):
        try:
            self.conn.ping()
        except:
            self.conn.ping(True)
        cur = self.conn.cursor()
        sql = " insert into pc_infor(name,comment_num,url,price,img_url) values ('"\
              + str(item['title'][0]) + "', '"\
              + str(item['comment_num'][0])+"', '"\
              + str(item['link'])+"', '"\
              + str(item['price'][0])+"', '"\
              + str(item['img_url'][0])+"')"
        try:
            cur.execute(sql)
            self.conn.commit()
        except Exception, e:
            log.msg("mysql error " + str(e), _level=logging.ERROR)
        cur.close()

        name = item['title'][0]
        price = item['price'][0]
        comment_num = item['comment_num'][0]
        url = item['link']
        img_url = item['img_url'][0]

        print u'商品名称:'+name
        print u'商品评论:'+comment_num
        print u'商品价格:'+price
        print u'商品链接:'+url
        print u'商品图片:'+img_url
        print '--------------------------------'
        return item

    def __del__(self):
        self.conn.close()
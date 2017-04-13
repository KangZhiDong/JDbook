# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

#
# class BooksPipeline(object):
#     def process_item(self, item, spider):
#         return item


import MySQLdb

class BooksPipeline(object):

    def process_item(self, item, spider):

        DBKWARGS = spider.settings.get('DBKWARGS')
        con = MySQLdb.connect(**DBKWARGS)
        cur = con.cursor()
        sql = ("insert into book(title,price,content,bookurl)"
               " values(%s,%s,%s,%s)")
        lis = (item['title'],item['price'],item['content'],item['bookurl'])
        try:
            cur.execute(sql,lis)
        except Exception,e:
            print "Insert error:",e
            con.rollback()
        else:
            con.commit()
        cur.close()
        con.close()
        return item
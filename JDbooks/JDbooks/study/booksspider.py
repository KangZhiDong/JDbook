# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import Selector
from books.items import BooksItem

class book(CrawlSpider):
    name = "book"
    start_urls = ['http://www.oreilly.com.cn/index.php?func=completelist']
    url = 'http://www.oreilly.com.cn/index.php?func=completelist'

    def parse(self,response):

        item = BooksItem()
        selector = Selector(response)
        books = selector.xpath('//a[@class="tip"]')

        for book in books:
            title = book.xpath('./text()').extract()
            item['title'] = title
            id = book.xpath('./@href').extract()
            id = id[0]
            whichbook = "http://www.oreilly.com.cn/{}".format(str(id))
            item['content']=whichbook
            yield item

#             yield  scrapy.Request(url=whichbook,callback=self.detail_parse,
#                                      meta={"title":title})
        nextLink = selector.xpath('//div[@class="plain_page"]/div/span/span/a/@href').extract()
        #第10页是最后一页，没有下一页的链接
        if nextLink:
            nextLink = nextLink[0]
            print nextLink
            yield Request(self.url + nextLink,callback=self.parse)


#             def detail_parse(self, response):
#                 selector = Selector(response)
#                 reads = selector.xpath('//*[@id="toc"]/ol/li').extract()
#
#
#                 item['title']=response.meta["title"]
#                 item['content'] = reads
#                 yield item
# pass




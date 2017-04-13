# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import Selector
from books.items import BooksItem
from lxml import etree
import json;
from selenium import webdriver

class book(CrawlSpider):
    name = "book"
    start_urls = ['https://channel.jd.com/1713-3287.html']
    url = 'https://channel.jd.com/1713-3287.html'

    def parse(self,response):


        selector = Selector(response)
        books = selector.xpath('//*[@id="p-category"]/div/div/div/div/h3')

        for book in books:

            id = book.xpath('./a/@href').extract().pop().split('.')[3]
            whichbooks = "https://list.jd.com/list.{}".format(str(id))

            yield  scrapy.Request(url=whichbooks , callback=self.book_parse)



    def book_parse(self,response):


            selector = Selector(response)
            reads = selector.xpath('//*[@id="plist"]/ul/li')
            for read in reads:
                try:
                    title = read.xpath('./div/div[3]/a/em/text()').extract()
                    whichbook_id = read.xpath('./div/@data-sku').extract()
                    str_convert = ''.join(whichbook_id)

                    # [0].encode('utf-8')
                    #whichbook = "https://item.jd.com/{}.html".format(str(str_convert))
                    priceurl = "https://p.3.cn/prices/mgets?skuIds=J_{}".format(str(str_convert))
                    #priceurl ="https://p.3.cn/prices/mgets?skuIds=J_11252778"
                    #r = requests.get(priceurl);

                    #price = r.m  # 解析p的值，即价格
                    # jsonString = response.read();
                    # jsonObject = json.loads(jsonString.decode())
                    #priceurl = "http://p.3.cn/prices/mgets?skuIds=J_{}".format(str(response.meta["str_convert"]))
                    #prices = json.loads(priceurl)
                    #price = prices['m']
                    #price = 123
                    yield scrapy.Request(url=priceurl, callback=self.price_parse, meta = {"title":title, "str_convert":str_convert})
                except Exception:
                    pass

            nextLink = selector.xpath('//*[@id="J_bottomPage"]/span[1]/a[10]/@href').extract()
            if nextLink:
                nextLink = nextLink[0]
                print nextLink
                yield Request('http://list.jd.com' + nextLink, callback=self.book_parse)

    def price_parse(self, response):

            #priceurl = "https://p.3.cn/prices/mgets?skuIds=J_{}".format(str(str_convert))
            #priceurl ="https://p.3.cn/prices/mgets?skuIds=J_11252778"
            #r = requests;
            sites = json.loads(response.body_as_unicode())
            for site in sites:
                #print site['m']
                price = site['m']
                whichbook = "https://item.jd.com/{}.html".format(str( response.meta["str_convert"]))

                yield scrapy.Request(url=whichbook, callback=self.detail_parse,
                                 meta={"title": response.meta["title"], "bookurl": whichbook, "str_convert": response.meta["str_convert"],"price": price})


    def detail_parse(self, response):
            item = BooksItem()

            selector = Selector(response)
            #http://p.3.cn/prices/mgets?skuIds=J_11252778,J_&type=1
            #price = selector.xpath('//*[@id="page_maprice"]/text()').extract()
            #content = selector.xpath('//*[@id="detail-tag-id-6"]/div[2]/div/text()').extract()
            #.pop().replace("<br>", " ")

            # with Browser() as browser:
            #     # Visit URL
            #     executable_path = {'executable_path': '/usr/local/Cellar/phantomjs/2.1.1/bin/phantomjs'}
            #     browser = Browser('phantomjs', **executable_path)
            #repr


            # driver.execute_script("window.scrollBy(0,5000)")
            # time.sleep(4)
            # time.sleep(4)
            # content = driver.find_elements_by_class_name(book-detail-content)
            # driver = webdriver.Chrome()





            bookurl = response.meta["bookurl"]
            driver = webdriver.PhantomJS()
            driver.get(bookurl)
            content = driver.find_element_by_xpath('//*[@id="detail-tag-id-6"]/div[2]/div').text
            driver.close()
            #content = 123


            try:
                item['title'] = response.meta["title"]
                item['price'] = response.meta["price"]
                item['content'] = content
                item['bookurl'] = response.meta["bookurl"]
                yield item
            except Exception:
                pass







                    # import urllib.request;  #载入urllib.request,用于获取页面html源代码
# from pandas import Series;  #载入series包
# from pandas import DataFrame;   #载入dataframe包
# from bs4 import BeautifulSoup;  #载入beautifulsoup包
# import json; #载入json包
#
# response = urllib.request.urlopen('http://item.jd.com/2957726.html'); #获取html源代码
# html = response.read(); #将源代码转入html
# soup = BeautifulSoup(html); #解析html
# data = DataFrame(columns=['Feature', 'Property']) #创建空白dataframe用于装载爬取信息
#
# divSoup = soup.find(id="product-detail-2")  #通过分析，发现规格参数所在部分id
# trs = divSoup.find_all('tr');
#
# for tr in trs :
#     tds = tr.find_all('td');
#     if len(tds)==2: #列表有两个值的时才执行爬取
#         f=tds[0].getText();
#         p=tds[1].getText();
#         data = data.append(
#             Series(
#                 [f, p],
#                 index=['Feature', 'Property']
#             ), ignore_index=True
#         );
#
# response = urllib.request.urlopen('http://p.3.cn/prices/get?skuid=J_2244423');
# jsonString = response.read();
# jsonObject = json.loads(jsonString.decode())
# jsonObject[0]['p']  #解析p的值，即价格
#
# df.to_csv("D:\\df.csv"); #导出结果
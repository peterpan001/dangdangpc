# -*- coding:utf-8 -*-
import scrapy
from dangdangpc.items import DangdangpcItem
from scrapy.http import Request

class PcSpider(scrapy.Spider):
    name = "pcdangdang_spider"
    allowed_domins = ['dongdong.com']
    start_urls = ['http://3c.dangdang.com/pc']

    def parse(self, response):#取出所有商品分类
        categroy = response.xpath('//div[@class="level_one "]/dl/dd/a/@href').extract()
        #print categroy
        for url in categroy:
            yield Request(url, callback=self.parse_detail)

    def parse_detail(self, response):
        link = response.xpath('//a[@class="pic"]/@href').extract()
        next_link = response.xpath('//li[@class="next"]/a/@href')[0].extract()
        if next_link:
            yield Request('http://category.dangdang.com/'+next_link, callback=self.parse_detail)

        for detail_url in link:
            yield Request(detail_url, callback=self.parse_price)

    def parse_price(self, response):
        item = DangdangpcItem()
        item['title'] = response.xpath('//div[@class="name_info"]/h1/@title').extract()
        item['price'] = response.xpath('//p[@id="dd-price"]/text()').extract()
        item['comment_num'] = response.xpath('//a[@id="comm_num_down"]/text()').extract()
        item['link'] = response.url
        item['img_url'] = response.xpath('//img[@id="modalBigImg"]/@src').extract()
        yield item




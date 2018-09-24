# -*- coding: utf-8 -*-
import scrapy
from mm131.items import Mm131Item


class Mm131Spider(scrapy.Spider):
    name = "mm131"
    allowed_domains = ["www.mm131.com"]
    start_urls = ['http://www.mm131.com/xiaohua/']

    def parse(self, response):
        list = response.xpath("//dl[contains(@class,'list-left')]/dd[not(@class='page')]")
        for content in list:
            contentUrl = str(content.xpath("a/@href").extract_first())
            yield scrapy.Request(contentUrl, callback=self.content)

        next_url = response.xpath("//dl[contains(@class,'list-left')]/dd[@class='page'] "
                                  "/a[contains(text(),'下一页')]/@href").extract_first()
        if next_url is not None:
            yield response.follow(next_url, callback=self.parse)

    def content(self, response):
        item = Mm131Item()
        item['name'] = response.xpath("//div[@class='content']/h5/text()").extract_first()
        item['refUrl']=response.url
        item['imgUrl'] = response.xpath("//div[@class='content-pic']/a/img/@src").extract_first()
        yield item
        next_url=response.xpath("//div[@class='content-page']/a[@class='page-ch' and contains(text(),'下一页')]/@href").extract_first()
        if next_url is not None:
            yield response.follow(next_url, callback=self.content)
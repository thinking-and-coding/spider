# -*- coding: utf-8 -*-
import scrapy

from spider.items import DoubanItem
from spider.string_utils import format_string


class Top250Spider(scrapy.Spider):
    name = 'top250'
    allowed_domains = ['movie.douban.com/top250']
    start_urls = ['https://movie.douban.com/top250']

    def parse(self, response):
        # 解析内容
        movie_list = response.xpath('//*[@class="item"]')
        for movie in movie_list:
            item = DoubanItem()
            item['title'] = format_string(movie.xpath('./div[@class="info"]/div[1]/a/span[1]/text()').extract_first())
            item['pic'] = format_string(movie.xpath('./div[@class="pic"]/a/img/@src').extract_first())
            item['link'] = format_string(movie.xpath('./div[@class="pic"]/a/@href').extract_first())
            item['actor'] = format_string(movie.xpath('./div[@class="info"]/div[2]/p[1]/text()').extract_first())
            item['score'] = format_string(movie.xpath('./div[@class="info"]/div[2]/div/span[2]/text()').extract_first())
            item['comments'] = format_string(movie.xpath('./div[@class="info"]/div[2]/div/span[4]/text()').extract_first())
            item['quota'] = format_string(movie.xpath('./div[@class="info"]/div[2]/p[2]/span/text()').extract_first())
            yield item
        # 查找下一页
        next_url = response.xpath('//span[@class="next"]/a/@href').extract_first()
        if next_url is not None:
            next_url = response.urljoin(next_url)
            yield scrapy.Request(url=next_url, callback=self.parse, dont_filter=True)

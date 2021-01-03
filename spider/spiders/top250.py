# -*- coding: utf-8 -*-
import scrapy
from spider.items import DoubanItem


class Top250Spider(scrapy.Spider):
    name = 'top250'
    allowed_domains = ['spider.com/']
    start_urls = ['https://movie.douban.com/top250']

    def parse(self, response):
        # 解析内容
        movie_list = response.xpath('//*[@class="item"]')
        for movie in movie_list:
            item = DoubanItem()
            item['title'] = self.fomatStr(movie.xpath('./div[@class="info"]/div[1]/a/span[1]/text()').extract_first())
            item['pic'] = self.fomatStr(movie.xpath('./div[@class="pic"]/a/img/@src').extract_first())
            item['link'] = self.fomatStr(movie.xpath('./div[@class="pic"]/a/@href').extract_first())
            item['actor'] = self.fomatStr(movie.xpath('./div[@class="info"]/div[2]/p[1]/text()').extract_first())
            item['score'] = self.fomatStr(movie.xpath('./div[@class="info"]/div[2]/div/span[2]/text()').extract_first())
            item['comments'] = self.fomatStr(movie.xpath('./div[@class="info"]/div[2]/div/span[4]/text()').extract_first())
            item['quota'] = self.fomatStr(movie.xpath('./div[@class="info"]/div[2]/p[2]/span/text()').extract_first())
            yield item
        # 查找下一页
        next_url = response.xpath('//span[@class="next"]/a/@href').extract_first()
        if next_url is not None:
            next_url = response.urljoin(next_url)
            yield scrapy.Request(url=next_url, callback=self.parse, dont_filter=True)

    # 格式化字符串，替换html格式空格同时去掉前后空格
    @staticmethod
    def fomatStr(str):
        if str is not None:
            return str.replace(' ', ' ').strip()
        return ''

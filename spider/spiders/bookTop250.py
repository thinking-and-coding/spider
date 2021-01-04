# -*- coding: utf-8 -*-
import scrapy
from spider.items import DoubanBookItem


class Booktop250Spider(scrapy.Spider):
    name = 'bookTop250'
    allowed_domains = ['book.douban.com/top250']
    start_urls = ['http://book.douban.com/top250/']

    def parse(self, response):
        # 解析内容
        movie_list = response.xpath('//tr[@class="item"]')
        for movie in movie_list:
            item = DoubanBookItem()
            item['title'] = self.fomatStr(movie.xpath('./td[2]/div[1]/a/@title').extract_first())
            item['pic'] = self.fomatStr(movie.xpath('./td[1]/a/img/@src').extract_first())
            item['link'] = self.fomatStr(movie.xpath('./td[2]/div[1]/a/@href').extract_first())
            item['author'] = self.fomatStr(movie.xpath('./td[2]/p[@class="pl"]/text()').extract_first().split('/')[0])
            item['score'] = self.fomatStr(movie.xpath('./td[2]/div[2]/span[@class="rating_nums"]/text()').extract_first())
            item['comments'] = self.fomatStr(
                movie.xpath('./td[2]/div[2]/span[@class="pl"]/text()').extract_first()[2:-2])
            item['quota'] = self.fomatStr(movie.xpath('./td[2]/p[@class="quote"]/span/text()').extract_first())
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

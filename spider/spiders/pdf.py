# -*- coding: utf-8 -*-
import scrapy

from spider.items import pdfItem


class PdfSpider(scrapy.Spider):
    name = 'pdf'
    allowed_domains = ['yun.weicheng.men']
    start_urls = ['https://yun.weicheng.men/?dir=Book']

    def parse(self, response):
        # 解析内容
        file_list = response.xpath('//li[position()>1]')
        for file in file_list:
            pdf = pdfItem()
            pdf['title'] = self.fomatStr(file.xpath('./@data-name').extract_first())
            pdf['link'] = response.urljoin(self.fomatStr(file.xpath('./a/@href').extract_first()))
            yield pdf
        # 当前无下页则不需要构造下一页请求


    # 格式化字符串，替换html格式空格同时去掉前后空格
    @staticmethod
    def fomatStr(str):
        if str is not None:
            return str.replace(' ', ' ').strip()
        return ''

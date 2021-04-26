# -*- coding: utf-8 -*-
import scrapy

from spider.items import pdfItem
from spider.string_utils import format_string


class PdfSpider(scrapy.Spider):
    name = 'pdf'
    allowed_domains = ['yun.weicheng.men']
    start_urls = ['https://yun.weicheng.men/?dir=Book']

    def parse(self, response, **kwargs):
        # 解析内容
        file_list = response.xpath('//li[position()>1]')
        for file in file_list:
            pdf = pdfItem()
            pdf['title'] = format_string(file.xpath('./@data-name').extract_first())
            pdf['link'] = response.urljoin(format_string(file.xpath('./a/@href').extract_first()))
            yield pdf
        # 当前无下页则不需要构造下一页请求
        pass

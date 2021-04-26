# -*- coding: utf-8 -*-
import scrapy

from spider.items import MavenItem
from spider.string_utils import format_string


class MavenSpider(scrapy.Spider):
    name = 'maven'
    allowed_domains = ['mvnrepository.com']
    start_urls = ['https://mvnrepository.com/popular']
    detail_url_prefix = 'https://mvnrepository.com/'

    def parse(self, response, **kwargs):
        # 解析内容
        artifactory_list = response.xpath('//div[@class="im"]')
        for artifactory in artifactory_list:
            item = MavenItem()
            # 列表页数据
            item['name'] = format_string(artifactory.xpath('./div[@class="im-header"]/h2[@class="im-title"]/a[@class=""]/text()').extract_first())
            item['description'] = format_string(artifactory.xpath('./div[@class="im-description"]/text()').extract_first())
            item['usages'] = format_string(artifactory.xpath('./div[@class="im-header"]/h2[@class="im-title"]/a[@class="im-usage"]/b').extract_first())
            item['link'] = self.detail_url_prefix + format_string(artifactory.xpath('./div[@class="im-header"]/h2[@class="im-title"]/a[@class=""]/@href').extract_first())
            # 如果获取到详情页
            if 'artifact' in item['link']:
                # 请求详情页
                yield scrapy.Request(item["href"], callback=self.parse_detail, meta={"item": item})
            yield item
        # 查找下一页
        next_url = response.xpath('//*[@id="maincontent"]/ul[@class="search-nav"]/li[last()]/a/@href').extract_first()
        if next_url is not None:
            # 加上前缀
            next_url = 'https://mvnrepository.com/popular' + next_url
            yield scrapy.Request(url=next_url, callback=self.parse, dont_filter=True)

    # 获取详情页信息
    def parse_detail(self, response):
        item = response.meta["item"]
        # 获取详情页的内容、图片
        item["license"] = response.xpath("//*[@id='maincontent']/table[@class='grid']/tbody/tr[1]/td").extract()
        item["categories"] = response.xpath("//*[@id='maincontent']/table[@class='grid']/tbody/tr[2]/td").extract()
        item["tags"] = response.xpath("//*[@id='maincontent']/table[@class='grid']/tbody/tr[3]/td/a/text()").extract()
        # 详情页数据
        yield item
        # 处理引用数据
        cite_url = self.detail_url_prefix + response.xpath("//*[@id='maincontent']/table/tbody/tr[last()]/td/a/@href").extract()
        if cite_url is not None:
            yield scrapy.Request(url=cite_url, callback=self.parse_cite, meta={"item": item})

    def parse_cite(self, response):
        item = response.meta["item"]
        # 解析内容
        cite_list = response.xpath('//div[@class="im"]')
        for cite in cite_list:
            item["usedBy"].append(cite.xpath('./div[@class="im-header"]/h2[@class="im-title"]/a[@class=""]/text()').extract_first())
            cite_link = self.detail_url_prefix + format_string(cite.xpath('./div[@class="im-header"]/h2[@class="im-title"]/a[@class=""]/@href').extract_first())
            item['citeLink'] = cite_link;
            yield scrapy.Request(url=cite_link, callback=self.parse_detail, dont_filter=True)
        # 下一页
        next_page = cite_link + response.xpath(
            '//*[@id="maincontent"]/ul[@class="search-nav"]/li[12]/a/@href').extract_first()
        if next_page is not None:
            next_page = cite_link + next_page
            yield scrapy.Request(url=next_page, callback=self.parse_cite, meta={"item": item})
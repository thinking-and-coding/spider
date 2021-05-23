# -*- coding: utf-8 -*-
import scrapy
from scrapy.utils import spider

from spider.items import MavenItem
from spider.string_utils import format_string
from urllib.parse import urljoin

class MavenSpider(scrapy.Spider):
    name = 'maven'
    allowed_domains = ['mvnrepository.com']
    start_urls = ['https://mvnrepository.com/popular']
    popular_url_prefix = 'https://mvnrepository.com/popular'
    detail_url_prefix = 'https://mvnrepository.com'
    #spider.logger.setLevel('INFO')

    def parse(self, response, **kwargs):
        # 解析内容
        artifactory_list = response.xpath('//div[@class="im"]')
        for artifactory in artifactory_list:
            detail_link = format_string(artifactory.xpath('./div[@class="im-header"]/h2[@class="im-title"]/a[1]/@href').extract_first())
            # 拼接详情页
            detail_link = urljoin(self.detail_url_prefix, detail_link)
            # 如果获取到详情页
            if 'artifact' in detail_link:
                # 请求详情页
                yield scrapy.Request(detail_link, callback=self.parse_detail, priority=2)
        # 查找下一页
        next_url = response.xpath('//*[@id="maincontent"]/ul[@class="search-nav"]/li[last()]/a/@href').extract_first()
        if next_url is not None:
            # 拼接下一页
            next_url = urljoin(self.popular_url_prefix, next_url)
            yield scrapy.Request(url=next_url, callback=self.parse, dont_filter=True, priority=1)

    # 获取详情页信息
    def parse_detail(self, response):
        item = MavenItem()
        # 获取详情页数据
        item['name'] = format_string(response.xpath("//*[@id='maincontent']/div[@class='im']/div[@class='im-header']/h2/a/text()").extract_first())
        item['description'] = format_string(response.xpath("//*[@id='maincontent']/div[@class='im']/div[@class='im-description']/text()").extract_first())
        item['usages'] = int(format_string(response.xpath("//*[@id='maincontent']/table/tbody/tr[last()]/td/a/b/text()").extract_first().split('\n')[0]).replace(',', ''))
        item["license"] = format_string(response.xpath("//*[@id='maincontent']/table[@class='grid']/tbody/tr[1]/td/span/text()").extract_first())
        item["categories"] = format_string(response.xpath("//*[@id='maincontent']/table[@class='grid']/tbody/tr[2]/td/a/text()").extract_first())
        item["tags"] = format_string(response.xpath("//*[@id='maincontent']/table[@class='grid']/tbody/tr[3]/td/a/text()").extract_first())
        # 只处理引用大于10的数据
        if item['usages'] >= 10:
            # 处理引用数据
            cite_url = response.xpath("//*[@id='maincontent']/table/tbody/tr[last()]/td/a/@href").extract_first()
            if cite_url is not None:
                cite_url = urljoin(self.detail_url_prefix, cite_url)
                # 保存引用链接和被引数据
                item["cite_url"] = cite_url
                item["used"] = set()
                yield scrapy.Request(url=cite_url, callback=self.parse_cite, meta={"item": item}, priority=5)

    def parse_cite(self, response):
        item = response.meta["item"]
        # 解析内容
        cite_list = response.xpath('//div[@class="im"]')
        for cite in cite_list:
            cite_name = format_string(cite.xpath('./div[@class="im-header"]/h2[@class="im-title"]/a[1]/text()').extract_first())
            if cite_name is not None and len(cite_name) != 0:
                spider.logger.info(msg="|->cite_name:"+cite_name)
                item["used"].add(cite_name)
                # 当前的包详情
                detail_link = format_string(cite.xpath('./div[@class="im-header"]/h2[@class="im-title"]/a[1]/@href').extract_first())
                detail_link = urljoin(self.detail_url_prefix, detail_link)
                yield scrapy.Request(url=detail_link, callback=self.parse_detail, priority=2)
        # 下一页
        next_page = format_string(response.xpath('//*[@id="maincontent"]/ul[@class="search-nav"]/li[12]/a/@href').extract_first())
        if next_page is not None:
            cite_url = item["cite_url"]
            next_page = urljoin(cite_url, next_page)
            yield scrapy.Request(url=next_page, callback=self.parse_cite, meta={"item": item}, priority=4)
        else:
            # 没有下一页则说明当前页面数据采集完整了
            yield item

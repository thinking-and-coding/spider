# -*- coding: utf-8 -*-
import json

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
    custom_settings = {
        # 设置管道下载
        'ITEM_PIPELINES': {
            'spider.pipelines.mavenPipeline': 300,
            'spider.pipelines.MavenNeo4jPipeline': 301,
        },
        # Neo4j配置
        'NEO4J_URI': "localhost:7687",
        'NEO4J_USER': "neo4j",
        'NEO4J_PASSWORD': "123456",
        # 设置日志
        'LOG_FILE': './log.txt',
        'LOG_LEVEL': 'INFO',
        'LOG_STDOUT': 'True',
        # 设置优先队列
        'SCHEDULER_PRIORITY_QUEUE': 'queuelib.PriorityQueue',
    }
    # 设置最小引用数限制
    cite_limit = 1000

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
            spider.logger.info("|->parse.next_url:" + next_url)
            yield scrapy.Request(url=next_url, callback=self.parse, dont_filter=True, priority=1)

    # 获取详情页信息
    def parse_detail(self, response):
        item = MavenItem()
        # 获取详情页数据
        item['name'] = format_string(response.xpath("//*[@id='maincontent']/div[@class='im']/div[@class='im-header']/h2/a/text()").extract_first())
        item['description'] = format_string(response.xpath("//*[@id='maincontent']/div[@class='im']/div[@class='im-description']/text()").extract_first())
        item["license"] = format_string(response.xpath("//*[@id='maincontent']/table[@class='grid']/tbody/*/td/span[@class='b lic']/text()").extract_first())
        item["categories"] = response.xpath("//*[@id='maincontent']/table[@class='grid']/tbody/*/td/a[@class='b c']/text()").extract
        item["tags"] = response.xpath("//*[@id='maincontent']/table[@class='grid']/tbody/*/td/a[@class='b tag']/text()").extract
        usages_block = response.xpath("//*[@id='maincontent']/table/tbody/tr[last()]/td/a/b/text()").extract_first()
        if usages_block is not None:
            item['usages'] = int(format_string(usages_block.split('\n')[0]).replace(',', ''))
        else:
            item['usages'] = 0
        # 只处理引用大于引用限制的数据
        if item['usages'] >= MavenSpider.cite_limit:
            # 处理引用数据
            cite_url = response.xpath("//*[@id='maincontent']/table/tbody/tr[last()]/td/a/@href").extract_first()
            if cite_url is not None:
                cite_url = urljoin(self.detail_url_prefix, cite_url)
                # 保存引用链接和被引数据
                item["cite_url"] = cite_url
                item["used"] = set()
                spider.logger.info("|->parse_detail.cite_url:" + cite_url)
                yield scrapy.Request(url=cite_url, callback=self.parse_cite, meta={"item": item}, priority=4)

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
                spider.logger.info("|->parse_cite.detail_link:" + detail_link)
                yield scrapy.Request(url=detail_link, callback=self.parse_detail, priority=3)
        # 下一页
        next_page = format_string(response.xpath('//*[@id="maincontent"]/ul[@class="search-nav"]/li[last()]/a/@href').extract_first())
        if next_page is not None:
            cite_url = item["cite_url"]
            next_page = urljoin(cite_url, next_page)
            delta_priority = next_page.split('=')[-1:]
            spider.logger.info("|->parse_cite.next_page:" + next_page + "delta_priority:" + delta_priority)
            yield scrapy.Request(url=next_page, callback=self.parse_cite, meta={"item": item}, priority=5+int(delta_priority))
        else:
            # 没有下一页则说明当前页面数据采集完整了
            spider.logger.info("|->parse_cite generate item finished！")
            yield item

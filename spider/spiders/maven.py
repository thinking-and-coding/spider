# -*- coding: utf-8 -*-
import scrapy

from spider.items import MavenItem
from spider.string_utils import format_string


class MavenSpider(scrapy.Spider):
    name = 'Maven'
    allowed_domains = ['mvnrepository.com']
    start_urls = ['https://mvnrepository.com/popular']
    detail_url_prefix = 'https://mvnrepository.com/'

    def parse(self, response):
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
        next_url = 'https://mvnrepository.com/popular' + response.xpath('//*[@id="maincontent"]/ul[@class="search-nav"]/li[12]/a/@href').extract_first()
        if next_url is not None:
            next_url = response.urljoin(next_url)
            yield scrapy.Request(url=next_url, callback=self.parse, dont_filter=True)

    def parse_detail(self,response):
        item = response.meta["item"]
        # 获取详情页的内容、图片
        item["license"] = response.xpath("//*[@id='maincontent']/table[@class='grid']/tbody/tr[1]/td").extract()
        item["categories"] = response.xpath("//*[@id='maincontent']/table[@class='grid']/tbody/tr[2]/td").extract()
        item["tags"] = response.xpath("//*[@id='maincontent']/table[@class='grid']/tbody/tr[3]/td/a/text()").extract()
        item["content_image"] = response.xpath(
            "//div[@class='wzy1']/table[2]//tr[1]/td[@class='txt16_3']//img/@src").extract()
        item["content_image"] = ["http://wz.sun0769.com" + i for i in item["content_image"]]
        yield item  # 对返回的数据进行处理
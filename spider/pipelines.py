# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json


class DoubanPipeline(object):
    def open_spider(self, spider):
        self.file = open('top250.json', 'w+')
        # 构造json格式数组
        self.file.write('[')

    def close_spider(self, spider):
        # 删除最后一个字符
        cursor = self.file.tell()
        if cursor > 3:
            self.file.seek(self.file.tell() - 2)
        # 构造json格式数组
        self.file.write(']')
        self.file.close()

    def process_item(self, item, spider):
        item = dict(item)
        print("|->movie:", item.get('title'))
        line = json.dumps(item, ensure_ascii=False) + ',\n'
        self.file.write(line)
        return item
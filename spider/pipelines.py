# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import urllib
from os.path import join, basename, dirname
from urllib.parse import urlparse

import scrapy
from neo4j import GraphDatabase
from scrapy.pipelines.files import FilesPipeline

from spider.settings import *


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


class DoubanBookPipeline(object):
    def open_spider(self, spider):
        self.file = open('bookTop250.json', 'w+')
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
        print("|->book:", item.get('title'))
        line = json.dumps(item, ensure_ascii=False) + ',\n'
        self.file.write(line)
        return item


class pdfPipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        yield scrapy.Request(item['link'], meta={'title': item['title']})

    def file_path(self, request, response=None, info=None, *, item=None):
        encode_path = urlparse(request.url).path
        decode_path = urllib.request.unquote(encode_path)
        print("|->decodePath:", decode_path)
        #return join(basename(dirname(decode_path)), basename(decode_path))
        # 此处直接返回文件名
        return basename(decode_path)


class mavenPipeline(FilesPipeline):
    def open_spider(self, spider):
        self.file = open('maven.json', 'w+')
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
        # set 转 list
        item['used'] = list(item['used'])
        item = dict(item)
        line = json.dumps(item, ensure_ascii=False) + ',\n'
        self.file.write(line)
        return item


class MavenNeo4jPipeline(object):
    # 建立neo4j的连接
    def __init__(self):
        self.driver = GraphDatabase.bolt_driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    def __del__(self):
        self.driver.close()

    def open_spider(self, spider):
        spider.logger.info(msg='建立neo4j数据库连接！')

    def close_spider(self, spider):
        spider.logger.info(msg='关闭neo4j数据库连接！')

    def process_item(self, item, spider):
        item = dict(item)
        spider.logger.info(msg='当前保存的数据：' + json.dumps(item))
        with self.driver.session() as session:
            # 保存节点全量信息
            session.write_transaction(self.merge_node_full, item)
            spider.logger.info(msg='保存节点数据完成，item：' + item.get("name"))
            # 保存引用节点信息(如果节点只有简单信息则需要保存其他完整信息)
            cite_list = item.get('used')
            if cite_list is not None and len(cite_list) != 0:
                for cite_node in cite_list:
                    session.write_transaction(self.merge_node_partial, cite_node)
                    spider.logger.info(msg='保存引用节点数据完成，item：' + cite_node)
                    # 保存关系
                    session.write_transaction(self.merge_relation, item.get("name"), cite_node)
                    spider.logger.info(msg='保存引用关系完成！')
        return item

    def merge_node_full(self, tx, item):
        return tx.run("MERGE (n:Item {name: $name,description: $description,usages:$usages,license:$license,"
               "categories:$categories,tags:$tags,cite_url:$cite_url})",
               name=item.get('name'), description=item.get('description'), usages=item.get('usages'),
               license=item.get('license'), categories=item.get('categories'), tags=item.get('tags'), cite_url=item.get('cite_url'))

    def merge_node_partial(self, tx, name):
        return tx.run("MERGE (n:Item {name: $name})", name=name)

    def merge_relation(self, tx, node, cite_node):
        return tx.run("MATCH (cite_node:Item{name:$cite_node}) "
                      "MATCH (node:Item{name:$node}) "
                      "MERGE (cite_node)-[:CITE]->(node)", node=node, cite_node=cite_node)

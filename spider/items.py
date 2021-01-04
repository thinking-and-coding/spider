# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item


class DoubanItem(Item):
    # define the fields for your item here like:
    # 电影标题
    title = Field()
    # 电影封面
    pic = Field()
    # 电影封面
    link = Field()
    # 演员
    actor = Field()
    # 评分
    score = Field()
    # 评论数
    comments = Field()
    # 总结
    quota = Field()

class DoubanBookItem(Item):
    # define the fields for your item here like:
    # 图书标题
    title = Field()
    # 图书封面
    pic = Field()
    # 图书链接
    link = Field()
    # 作者
    author = Field()
    # 评分
    score = Field()
    # 评论数
    comments = Field()
    # 总结
    quota = Field()

class pdfItem(Item):
    # define the fields for your item here like:
    # pdf标题
    title = Field()
    # pdf链接
    link = Field()

# spider
一些爬虫
基于python3.6、scrapy开发的爬虫

使用方法：1.找到代码文件路径，使用终端进入到spider目录下 cd spider 2.输入 scrapy crawl top250 --nolog 开始爬取。3.数据输出到top250.json文件(爬取结果已附在代码库中)

目前拥有的爬虫：豆瓣电影评分top250爬虫(top250.py)、豆瓣图书评分top250爬虫(bookTop250.py)

爬行命令：
开启缓存队列，避免爬行中断
scrapy crawl maven -s JOBDIR=./queue

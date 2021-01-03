# spider
一些爬虫
基于python3.6、scrapy、neo4j开发的爬虫  
其中，豆瓣社交关系爬虫使用neo4j图数据库进行存储

使用方法：1.找到代码文件路径，使用终端进入到spider目录下 cd spider 2.输入 scrapy crawl top250 --nolog 开始爬取。3.数据输出到top250.json文件(爬取结果已附在代码库中)

目前拥有的爬虫：豆瓣电影评分top250爬虫(top250.py)、豆瓣社交关系爬虫

注意:豆瓣登录态关注dbcl2这个cookie
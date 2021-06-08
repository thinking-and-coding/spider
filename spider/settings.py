# -*- coding: utf-8 -*-

# Scrapy settings for spider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html
from spider.user_agent import get_random_agent

BOT_NAME = 'spider'

SPIDER_MODULES = ['spider.spiders']
NEWSPIDER_MODULE = 'spider.spiders'

# 设置日志
#LOG_FILE = './log.txt'
LOG_LEVEL = 'INFO'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = get_random_agent()
#USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36'


# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
#    'Accept': '*/*',
#    'Accept-Language': 'zh',
#    'Cookie': '__cfduid=d91a02f11c7ffb5f5095ff314a0881e171609764833'
    'origin':'https://mvnrepository.com/',
    'referer':'https://mvnrepository.com/'
}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'spider.middlewares.DoubanSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
#    'spider.middlewares.DoubanDownloaderMiddleware': 543,
    'spider.middlewares.SeleniumMiddleware': 543,
#    'scrapy_cloudflare_middleware.middlewares.CloudFlareMiddleware': 560
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    #'spider.pipelines.DoubanPipeline': 300,
    #'spider.pipelines.DoubanBookPipeline': 300,
    #'spider.pipelines.pdfPipeline': 300,
    #'spider.pipelines.pdfPipeline': 300,
    #'spider.pipelines.mavenPipeline': 300,
    #'spider.pipelines.MavenNeo4jPipeline': 301,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
HTTPCACHE_IGNORE_HTTP_CODES = [403]
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# 文件下载路径
FILES_STORE = './Download/pdf'

# 中间件配置
SELENIUM_TIMEOUT = 10
#PHANTOMJS_SERVICE_ARGS = ['--load-images=false','--disk-cache=true']
PHANTOMJS_SERVICE_ARGS = []

# 爬虫允许的最大深度，可以通过meta查看当前深度；0表示无深度
# DEPTH_LIMIT = 0

# 爬取时，0表示深度优先Lifo(默认)；1表示广度优先FiFo
# 后进先出，深度优先
# DEPTH_PRIORITY = 0
# SCHEDULER_DISK_QUEUE = 'scrapy.squeues.PickleLifoDiskQueue'
# SCHEDULER_MEMORY_QUEUE = 'scrapy.squeues.LifoMemoryQueue'

# 先进先出，广度优先
#DEPTH_PRIORITY = 1
#SCHEDULER_DISK_QUEUE = 'scrapy.squeues.PickleFifoDiskQueue'
#SCHEDULER_MEMORY_QUEUE = 'scrapy.squeues.FifoMemoryQueue'

# Neo4j配置
NEO4J_URI = "localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "123456"


# Enables scheduling storing requests queue in redis.
SCHEDULER = "scrapy_redis.scheduler.Scheduler"

# Ensure all spiders share same duplicates filter through redis.
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

# Enables stats shared based on Redis
STATS_CLASS = "scrapy_redis.stats.RedisStatsCollector"

# Default requests serializer is pickle, but it can be changed to any module
# with loads and dumps functions. Note that pickle is not compatible between
# python versions.
# Caveat: In python 3.x, the serializer must return strings keys and support
# bytes as values. Because of this reason the json or msgpack module will not
# work by default. In python 2.x there is no such issue and you can use
# 'json' or 'msgpack' as serializers.
#SCHEDULER_SERIALIZER = "scrapy_redis.picklecompat"

# Don't cleanup redis queues, allows to pause/resume crawls.
SCHEDULER_PERSIST = True

# Schedule requests using a priority queue. (default)
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.PriorityQueue'

# Alternative queues.
#SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.FifoQueue'
#SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.LifoQueue'

# Max idle time to prevent the spider from being closed when distributed crawling.
# This only works if queue class is SpiderQueue or SpiderStack,
# and may also block the same time when your spider start at the first time (because the queue is empty).
SCHEDULER_IDLE_BEFORE_CLOSE = 60

# Maximum idle time before close spider.
# When the number of idle seconds is greater than MAX_IDLE_TIME_BEFORE_CLOSE, the crawler will close.
# If 0, the crawler will DontClose forever to wait for the next request.
# If negative number, the crawler will immediately close when the queue is empty, just like Scrapy.
MAX_IDLE_TIME_BEFORE_CLOSE = 60

# Store scraped item in redis for post-processing.
ITEM_PIPELINES = {
    'scrapy_redis.pipelines.RedisPipeline': 300,
    'spider.pipelines.MavenNeo4jPipeline': 301,
}

# The item pipeline serializes and stores the items in this redis key.
#REDIS_ITEMS_KEY = '%(spider)s:items'

# The items serializer is by default ScrapyJSONEncoder. You can use any
# importable path to a callable object.
#REDIS_ITEMS_SERIALIZER = 'json.dumps'

# Specify the host and port to use when connecting to Redis (optional).
REDIS_HOST = 'localhost'
REDIS_PORT = 6379

# Specify the full Redis URL for connecting (optional).
# If set, this takes precedence over the REDIS_HOST and REDIS_PORT settings.
#REDIS_URL = 'redis://user:pass@hostname:9001'

# Custom redis client parameters (i.e.: socket timeout, etc.)
#REDIS_PARAMS  = {}
# Use custom redis client class.
#REDIS_PARAMS['redis_cls'] = 'myproject.RedisClient'

# If True, it uses redis' ``SPOP`` operation. You have to use the ``SADD``
# command to add URLs to the redis queue. This could be useful if you
# want to avoid duplicates in your start urls list and the order of
# processing does not matter.
#REDIS_START_URLS_AS_SET = False

# If True, it uses redis ``zrevrange`` and ``zremrangebyrank`` operation. You have to use the ``zadd``
# command to add URLS and Scores to redis queue. This could be useful if you
# want to use priority and avoid duplicates in your start urls list.
REDIS_START_URLS_AS_ZSET = True

# Default start urls key for RedisSpider and RedisCrawlSpider.
REDIS_START_URLS_KEY = 'maven:start_urls'

# Use other encoding than utf-8 for redis.
#REDIS_ENCODING = 'latin1'

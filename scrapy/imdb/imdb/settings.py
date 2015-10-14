# -*- coding: utf-8 -*-

# Scrapy settings for imdb project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'imdb'

SPIDER_MODULES = ['imdb.spiders']
NEWSPIDER_MODULE = 'imdb.spiders'
# START_URLS = ["http://www.imdb.com/chart/top"]

START_URLS = ["http://www.imdb.com/chart/toptv"]
# START_URLS = ["http://www.imdb.com/list/ls003454917/"]


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'imdb (+http://www.yourdomain.com)'


ITEM_PIPELINES = {'imdb.pipelines.ImdbPipeline':100,
                            }

MONGODB_SERVER = "localhost"
MONGODB_PORT = 27017
MONGODB_DB = "Quotable"

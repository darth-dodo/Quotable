# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ImdbItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    list_ranking = scrapy.Field()
    imdb_id = scrapy.Field()
    name = scrapy.Field()
    quotes = scrapy.Field()
    trivia = scrapy.Field()
    rating = scrapy.Field()
    cast = scrapy.Field()
    rating = scrapy.Field()
    description = scrapy.Field()
    director = scrapy.Field()
    img_src = scrapy.Field()

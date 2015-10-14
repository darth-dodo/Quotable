# -*- coding: utf-8 -*-
import scrapy
from scrapy.conf import settings
from scrapy.selector import Selector
from scrapy.http.request import Request
from imdb.items import ImdbItem
# import requests
# from bs4 import BeautifulSoup
from imdb_quote import quote_spider

class ImdbListSpider(scrapy.Spider):
    name = "imdb_list"
    allowed_domains = ["imdb.com"]
    start_urls = settings['START_URLS']
    print start_urls

    base = "http://www.imdb.com/"

    def parse(self, response):

        sel = Selector(response)
        all_urls = sel.xpath("//td[@class='titleColumn']/a/@href").extract()
        all_movies_urls = []

        for url in all_urls:
            all_movies_urls.append(self.base + url)

        for movies_url in all_movies_urls:
            yield Request(movies_url, callback=self.parse_movie)

    def parse_movie(self, response):
        mov_sel = Selector(response)
        item = ImdbItem()
        m_id = response.request.url.split('/')[5]
        item['imdb_id'] = m_id
        item['name'] = self.get_movie_name(mov_sel)
        item['rating'] = self.get_rating(mov_sel)
        item['description'] = self.get_description(mov_sel)
        item['director'] = self.get_director(mov_sel)
        # item['quotes'] = self.get_quotes(m_id)
        item['img_src'] = self.get_img_src(mov_sel)


        # bs4
        item['quotes'] = quote_spider(m_id)


        # print len(item['quotes'])
        print item
        return item

    def trim(self, raw_str):

        return raw_str.encode('ascii', errors='ignore').strip()

    def trim_list(self, raw_list):

        return [self.trim(raw_str) for raw_str in raw_list]


    def get_movie_name(self, selector):

        movie_name = selector.xpath(
            '//h1[@class="header"]/span[@itemprop ="name"]/text()').extract()[0]

        return self.trim(movie_name)


    def get_rating(self, selector):

        rating = selector.xpath(
            '//span[@itemprop="ratingValue"]/text()').extract()[0]

        return float(self.trim(rating))


    def get_description(self, selector):
        """
        Extracts the movie description (short excerpt).
        """
        description = selector.xpath(
            '//td[@id="overview-top"]/p[@itemprop="description"]/text()').extract()[0]

        return self.trim(description)

    def get_director(self, selector):
        """
        Name(s) of the director(s).
        """
        director = selector.xpath(
            '//div[@itemprop="director"]/a/span[@itemprop="name"]/text()').extract()

        return self.trim_list(director)


    def get_img_src(self, selector):
        img_src = selector.xpath('//div[@class="image"]/a/img[@itemprop="image"]/@src').extract()[0]
        return self.trim(img_src)



    # def get_quotes(self, imdb_id):

    #     url = self.base + 'title/' + imdb_id + "/quotes"
    #     source_code = requests.get(url)
    #     plain_text = source_code.text
    #     soup = BeautifulSoup(plain_text)
    #     app = []
    #     for quote in soup.findAll('div', {'class': 'sodatext'}):
    #         a = (quote.text).encode('utf-8')
    #         return self.trim(a)









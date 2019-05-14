# -*- coding: utf-8 -*-
import scrapy
from ..items import HdrezkaItem


class HdrezkaSpider(scrapy.Spider):
    name = 'hdrezka'
    start_urls = ['https://rezka.ag/new/page/1/']
    page_number = 2

    def parse(self, response):

        urls = response.css('.b-content__inline_item-link a::attr(href)').getall()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_films)

        n = range(3, 21, 1)
        i = n[0]

        next_page_url = 'https://rezka.ag/new/page/{}/'.format(HdrezkaSpider.page_number)
        HdrezkaSpider.page_number += 1

        if next_page_url:
            if HdrezkaSpider.page_number < 21:
                yield scrapy.Request(url=next_page_url, callback=self.parse)

    def parse_films(self, response):
        items = HdrezkaItem()

        items['name'] = response.css('h1::text').get()
        items['date'] = data_choose(response)

        items['rating'] = {
            'IMDb': None,
            'Кинопоиск': None
        }
        IMDb = response.css('.imdb .bold::text').get()
        Kp = response.css('.kp .bold::text').get()
        if IMDb:
            items['rating']['IMDb'] = IMDb
        if Kp:
            items['rating']['Кинопоиск'] = Kp

        director = response.css('.person-name-item').get()
        director = director.split('<')[-4].split('>')[-1]
        items['director'] = director

        items['genre'] = response.css('.b-post__info td > a span::text').getall()
        items['picture'] = response.css('.b-sidecover img::attr(src)').get()
        items['description'] = response.css('.b-post__description_text::text').get()

        yield items


def data_choose(response):
    month = ['января', 'февраля', 'марта',
             'апреля', 'мая', 'июня',
             'июля', 'авгуcта', 'сентября',
             'октября', 'ноября', 'февраля']
    numbers = [1, 2, 3, 4]
    for number in numbers:
        selector1 = 'tr:nth-child({}) .l+ td::text'.format(str(number))
        selector2 = 'tr:nth-child({}) a::text'.format(str(number))
        date = response.css(selector1).get()

        if date is not None and len(date.split()) > 1 and date.split()[1] in month:
            return response.css(selector1).get() + response.css(selector2).get()

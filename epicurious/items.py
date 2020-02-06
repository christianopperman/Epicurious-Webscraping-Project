# -*- coding: utf-8 -*-

import scrapy

class EpicuriousItem(scrapy.Item):
    recipe = scrapy.Field()
    url = scrapy.Field()
    rating = scrapy.Field()
    reviews = scrapy.Field()
    make_again = scrapy.Field()
    ingredients = scrapy.Field()
    calories = scrapy.Field()
    carbs = scrapy.Field()
    protein = scrapy.Field()
    fat = scrapy.Field()
    keywords = scrapy.Field()




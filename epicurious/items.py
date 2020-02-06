# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

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




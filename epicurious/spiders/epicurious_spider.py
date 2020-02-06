from scrapy import Spider, Request
from epicurious.items import EpicuriousItem
import re
import time

start = time.time()

class EpicuriousSpider(Spider):
    name = "epicurious_spider"
    allowed_urls = ["https://www.epicurious.com/"]
    start_urls = ["https://www.epicurious.com/search/?content=recipe"]

    # Crawls through the Epicurious recipe landing page. Identifies the total number of recipes and generates a 
    # list of URLs for each separate recipe aggregating page (each page has 18 recipe tiles on it).
    def parse(self, response):
        num_recipes = int(''.join(re.findall('\d+',response.xpath('//*[@class="matching-count"]/text()').extract_first())))
        recipes_per_page = 18

        total_pages = num_recipes//recipes_per_page
        if num_recipes % recipes_per_page != 0:
            total_pages += 1

        page_urls = [f'https://www.epicurious.com/search/?content=recipe&page={i+1}' for i in range(total_pages)]

        for url in page_urls:
            yield Request(url = url, callback = self.parse_recipe_page)

    # Cralws through each separate recipe aggregating page and generates a URL to each individual recipe page, as well
    # as the recipe name, rating (out of 4), total number of reviews, and the number of users who would make the recipe
    # again.
    def parse_recipe_page(self, response):
        cards = response.xpath('//article[@class="recipe-content-card"]')
        for card in cards:
            recipe = card.xpath('.//h4/a/text()').extract_first()
            url = f"https://epicurious.com{card.xpath('.//h4/a/@href').extract_first()}"
            rating = float(card.xpath('./header//dd/span[1]/text()').extract_first())
            reviews = int(card.xpath('.//*[@class="reviews-count"]/text()').extract_first())
            make_again = int(card.xpath('.//dd[@class="make-again-percentage"]/text()').extract_first())

            meta = {}
            meta['recipe'] = recipe
            meta['url'] = url
            meta['rating'] = rating
            meta['reviews'] = reviews
            meta['make_again'] = make_again

            yield Request(url = url, callback = self.parse_recipe, meta = meta)


    # Crawls through each individual recipe for identifying keywords, nutritional information, and ingredients.
    def parse_recipe(self, response):
        # Exception handling because not all recipes have nutritional information. No information instantialized as None
        try:
            calories = int(response.xpath('//div[@class="nutrition content"]//span[@itemprop="calories"]/text()').extract_first())
        except:
            calories = None
        
        try:
            carbs = int(re.findall('\d+', response.xpath('//div[@class="nutrition content"]//span[@itemprop="carbohydrateContent"]/text()').extract_first())[0])
        except:
            carbs = None

        try:
            protein = int(re.findall('\d+', response.xpath('//div[@class="nutrition content"]//span[@itemprop="proteinContent"]/text()').extract_first())[0])
        except:
            protein = None

        try:
            fat = int(re.findall('\d+', response.xpath('//div[@class="nutrition content"]//span[@itemprop="fatContent"]/text()').extract_first())[0])
        except:
            fat = None

        keywords = response.xpath('//meta[@name="keywords"]/@content').extract_first()
        ingredients = '\t'.join(response.xpath('//li[@class="ingredient"]/text()').extract())

        item = EpicuriousItem()
        item['recipe'] = response.meta['recipe']
        item['url'] = response.meta['url']
        item['rating'] = response.meta['rating']
        item['reviews'] = response.meta['reviews']
        item['make_again'] = response.meta['make_again']
        item['ingredients'] = ingredients
        item['calories'] = calories
        item['carbs'] = carbs
        item['protein'] = protein
        item['fat'] = fat
        item['keywords'] = keywords

        yield item

end = time.time()
print ('='*50)
print(end-start)
print ('='*50)


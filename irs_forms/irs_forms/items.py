# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class IrsFormsItem(scrapy.Item):
    file_urls = scrapy.Field()
    files = scrapy.Field()
    form_number = scrapy.Field()
    form_title = scrapy.Field()
    year = scrapy.Field()
    min_year = scrapy.Field()
    max_year = scrapy.Field()

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class IrsFormsPipeline:
    formArray = [{}]
    def process_item(self, item, spider):
        self.formArray[0] = item

    def close_spider(self, spider):
        print('result array: ', self.formArray)
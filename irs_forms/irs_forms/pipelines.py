# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import NotConfigured
import json
import requests
import os


class IrsFormsPipeline:
    form_array = []

    def open_spider(self, spider):
        print('opening spider: ', spider.name)
    
    def close_spider(self, spider):
        print('closing spider: ', spider.name)
        print('final array: ', self.form_array)
        formatted_array = json.dumps(self.form_array, indent=4)
        basepath = 'results'
        filename = 'form_info.json'
        os.makedirs(basepath, exist_ok=True)
        filepath = os.path.join(basepath, filename)
        with open(filepath, 'w') as file:
            file.write(formatted_array)

    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.getbool('IRS_FORMS_PIPELINE_ENABLED'):
            raise NotConfigured
        return cls()

    def process_item(self, item, spider):
        scrpd = ItemAdapter(item)
        f = (form for index,form in enumerate(self.form_array) if form.get('form_number') == scrpd['form_number'])
        i = (index for index,form in enumerate(self.form_array) if form.get('form_number') == scrpd['form_number'])
        form = next(f, None)
        index = next(i, None)
        if form:
            if scrpd['min_year'] < form['min_year']:
                form['min_year'] = scrpd['min_year']
            if scrpd['max_year'] > form['max_year']:
                form['max_year'] = scrpd['max_year']

            print('inserting item: ', form)
            self.form_array.pop(index)
            self.form_array.insert(index, dict(form))
        else:
            print('appending item: ', item)
            self.form_array.append(dict(item))

        return scrpd
        

class DownloadFormsPipeline:

    def open_spider(self, spider):
        print('opening spider: ', spider.name)

    def close_spider(self, spider):
        print('closing spider: ', spider.name)

    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.getbool('DOWNLOAD_FORMS_PIPELINE_ENABLED'):
            raise NotConfigured
        return cls()

    def process_item(self, item, spider):
        scrpd = ItemAdapter(item)
        response = requests.get(scrpd['file_urls'])
        form_number = scrpd['form_number']
        year = scrpd['year']

        basepath = os.path.join('results', form_number)
        filename = f'{form_number} - {year}.pdf'
        filepath = os.path.join(basepath, filename)
        
        os.makedirs(basepath, exist_ok=True)

        with open(filepath, 'wb') as file:
            file.write(response.content)
        return item

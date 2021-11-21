# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json


class IrsFormsPipeline:
    form_array = []

    def open_spider(self, spider):
        self.file = open('forms.json', 'w')
    
    def close_spider(self, spider):
        formatted_array = json.dumps(self.form_array, indent=4)
        self.file.write(formatted_array)
        self.file.close()

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

            self.form_array.pop(index)
            self.form_array.insert(index, form)
        else:
            self.form_array.append(scrpd)

        return scrpd
        

class DownloadFormsPipeline:
    
    def open_spider(self, spider):
        self.file = open('../form_downloads/', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        return item
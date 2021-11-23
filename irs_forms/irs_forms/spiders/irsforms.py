import scrapy
from ..items import IrsFormsItem

class IrsformsSpider(scrapy.Spider):
    name = 'irsforms'
    form_list = []
    url = ''
    form = IrsFormsItem()

    # make sure the only pipeline activated is the one associated with the running spider
    custom_settings = {
        'IRS_FORMS_PIPELINE_ENABLED': True,
        'DOWNLOAD_FORMS_PIPELINE_ENABLED': False
    }


    def start_requests(self):
        self.form_list = input('Enter form name(s) separated by commas, ie. W-2,1040,1099-A :').replace(' ', '').split(',')
        if len(self.form_list) == 1 and self.form_list[0] == '':
            print('ERROR: No form numbers entered')
            return None
        else:
            for form in self.form_list:
                if form:
                    self.url = f'https://apps.irs.gov/app/picklist/list/priorFormPublication.html?value=Form+{form}&criteria=formNumber'
                    yield scrapy.Request(url=self.url, callback=self.parse, cb_kwargs=dict(form=form))


    def parse(self, response, form):
        table_rows = response.xpath('//table[@class="picklist-dataTable"]/tr')
        next_page_link = response.xpath('//div[@class="paginationBottom"]/a[contains(text(), "Next")]/@href').get()
        next_page_absolute_url = response.urljoin(next_page_link)

        for row in table_rows:
            form_number = row.xpath('./td[@class="LeftCellSpacer"]/a/text()').get()

            if form_number == f'Form {form}':
                form_title = row.xpath('normalize-space(./td[@class="MiddleCellSpacer"]/text())').get()
                year = row.xpath('normalize-space(./td[@class="EndCellSpacer"]/text())').get()

                self.form['form_number'] = form_number
                self.form['form_title'] = form_title
                self.form['min_year'] = year
                self.form['max_year'] = year

                yield self.form
        
        if next_page_link:
            yield scrapy.Request(url=next_page_absolute_url, callback=self.parse, cb_kwargs=dict(form=form))




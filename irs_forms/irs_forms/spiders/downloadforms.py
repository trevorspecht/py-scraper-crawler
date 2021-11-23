import scrapy
from ..items import IrsFormsItem

class DownloadformsSpider(scrapy.Spider):
    name = 'downloadforms'
    custom_settings = {
        'IRS_FORMS_PIPELINE_ENABLED': False,
        'DOWNLOAD_FORMS_PIPELINE_ENABLED': True
    }
    url = ''
    years = []
    form = IrsFormsItem()
    form_number_input = ''
    input = []


    def start_requests(self):
        self.input = input('Enter a form number, a comma, and a year or range of years, ie. W-2,1995-2000 :').replace(' ', '').split(',')
        self.form_number_input = self.input[0]
        year_range = self.input[1]
        end_years = year_range.split('-')
        self.url = f'https://apps.irs.gov/app/picklist/list/priorFormPublication.html?value=Form+{self.form_number_input}&criteria=formNumber'


        # catch some year range user input edge cases
        if len(end_years) == 2 and end_years[0] == '':
            end_years.pop(0)
        if len(end_years) == 2 and end_years[1] == '':
            end_years.pop(1)
        if len(end_years) == 1:
            self.years.append(end_years[0])
        if len(end_years) == 2:
            for year in range(int(end_years[0]), int(end_years[1])+1):
                self.years.append(year)

        if not self.form_number_input:
            print('form number not entered')
            return None
        if not year_range:
            print('year range not entered')
            return None
        
        yield scrapy.Request(url=self.url, callback=self.parse)


    def parse(self, response):
        table_rows = response.xpath('//table[@class="picklist-dataTable"]/tr')
        next_page_link = response.xpath('//div[@class="paginationBottom"]/a[contains(text(), "Next")]/@href').get()
        next_page_absolute_url = response.urljoin(next_page_link)

        for row in table_rows:
            form_number = row.xpath('./td[@class="LeftCellSpacer"]/a/text()').get()
            form_link = row.xpath('./td[@class="LeftCellSpacer"]/a/@href').get()
            form_year = row.xpath('normalize-space(./td[@class="EndCellSpacer"]/text())').get()
            
            if form_number == f'Form {self.form_number_input}':
                for year in self.years:
                    year_str = str(year)
                    if year_str == form_year:
                        self.form['form_number'] = form_number
                        self.form['file_urls'] = form_link
                        self.form['year'] = year
                        yield self.form
        
        if next_page_link:
            yield scrapy.Request(url=next_page_absolute_url, callback=self.parse)

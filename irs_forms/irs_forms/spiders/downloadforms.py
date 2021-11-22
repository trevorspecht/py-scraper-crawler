import scrapy
from ..items import IrsFormsItem

class DownloadformsSpider(scrapy.Spider):
    name = 'downloadforms'
    form_number = '1099-A'
    year_range = '1990-2015'
    url = f'https://apps.irs.gov/app/picklist/list/priorFormPublication.html?value=Form+{form_number}&criteria=formNumber'
    years = []
    form = IrsFormsItem()

    custom_settings = {
        'IRS_FORMS_PIPELINE_ENABLED': False,
        'DOWNLOAD_FORMS_PIPELINE_ENABLED': True
    }

    end_years = year_range.split('-')
    for year in range(int(end_years[0]), int(end_years[1])+1):
        years.append(year)

    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse)


    def parse(self, response):
        table_rows = response.xpath('//table[@class="picklist-dataTable"]/tr')
        next_page_link = response.xpath('//div[@class="paginationBottom"]/a[contains(text(), "Next")]/@href').get()
        next_page_absolute_url = response.urljoin(next_page_link)

        for row in table_rows:
            form_number = row.xpath('./td[@class="LeftCellSpacer"]/a/text()').get()
            form_link = row.xpath('./td[@class="LeftCellSpacer"]/a/@href').get()
            form_year = row.xpath('normalize-space(./td[@class="EndCellSpacer"]/text())').get()
            
            for year in self.years:
                year_str = str(year)
                if year_str == form_year:
                    self.form['form_number'] = form_number
                    self.form['file_urls'] = form_link
                    self.form['year'] = year
                    yield self.form
        
        if next_page_link:
            yield scrapy.Request(url=next_page_absolute_url, callback=self.parse)


# import sys
# form_number = sys.argv[1]
# year_range = sys.argv[2]
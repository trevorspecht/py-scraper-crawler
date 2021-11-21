import scrapy


class DownloadformsSpider(scrapy.Spider):
    name = 'downloadforms'
    form_name = '706-NA'
    year_range = '1990-2000'

    form_years = year_range.split('-')

    def start_requests(self):
        url = f'https://apps.irs.gov/app/picklist/list/priorFormPublication.html?value=Form+{form}&criteria=formNumber'
        yield scrapy.Request(url=url, callback=self.parse, cb_kwargs=dict(form=form))

    def parse(self, response, form):

        for year in self.form_years:
            print(year)


        table_rows = response.xpath('//table[@class="picklist-dataTable"]/tr')
        next_page_link = response.xpath('//div[@class="paginationBottom"]/a[contains(text(), "Next")]/@href').get()
        next_page_absolute_url = response.urljoin(next_page_link)

        for row in table_rows:
            form_number = row.xpath('./td[@class="LeftCellSpacer"]/a/text()').get()

            if form_number == f'Form {form}':
                form_title = row.xpath('normalize-space(./td[@class="MiddleCellSpacer"]/text())').get()
                year = row.xpath('normalize-space(./td[@class="EndCellSpacer"]/text())').get()

                form_entry = {
                    # 'form_link': response.xpath('//td[has-class("LeftCellSpacer")]/a/@href').get(),
                    'form_number': form_number,
                    'form_title': form_title,
                    'min_year': year,
                    'max_year': year
                }

                yield form_entry
        
        if next_page_link:
            yield scrapy.Request(url=next_page_absolute_url, callback=self.parse, cb_kwargs=dict(form=form))




import scrapy


class IrsformsSpider(scrapy.Spider):
    name = 'irsforms'
    form_list = ['1099-A', '1095-C', '706-NA', 'W-2', '1040']
    result = []


    def start_requests(self):
        for form in self.form_list:
            url = 'https://apps.irs.gov/app/picklist/list/priorFormPublication.html?value=Form+{}&criteria=formNumber'.format(form)
            yield scrapy.Request(url=url, callback=self.parse, cb_kwargs=dict(form=form))


    def parse(self, response, form):
        table_rows = response.xpath('//table[@class="picklist-dataTable"]/tr')
        next_page_link = response.xpath('//div[@class="paginationBottom"]/a[contains(text(), "Next")]/@href').get()
        next_page_absolute_url = response.urljoin(next_page_link)

        for row in table_rows:
            form_number = row.xpath('./td[@class="LeftCellSpacer"]/a/text()').get()

            if form_number == 'Form {}'.format(form):
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




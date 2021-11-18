import scrapy


class IrsformsSpider(scrapy.Spider):
    name = 'irsforms'
    start_urls = ['https://apps.irs.gov/app/picklist/list/priorFormPublication.html/']
    page_count = 0

    def start_requests(self):
        urls = {
            # 'W-2': 'https://apps.irs.gov/app/picklist/list/priorFormPublication.html?value=Form+W-2&criteria=formNumber',
            '1040': 'https://apps.irs.gov/app/picklist/list/priorFormPublication.html?value=Form+1040&criteria=formNumber'
        }

        for name, url in urls.items():
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        table_rows = response.xpath('//table[@class="picklist-dataTable"]/tr')
        for row in table_rows:
            form_number = row.xpath('./td[has-class("LeftCellSpacer")]/a/text()').get()
            if form_number == 'Form 1040':
                yield {
                    # 'form_link': response.xpath('//td[has-class("LeftCellSpacer")]/a/@href').get(),
                    'form_number': form_number,
                    'form_title': row.xpath('normalize-space(./td[@class="MiddleCellSpacer"]/text())').get(),
                    'year': row.xpath('normalize-space(./td[@class="EndCellSpacer"]/text())').get()
                }

        next_page_link = response.xpath('//div[@class="paginationBottom"]/a[contains(text(), "Next")]/@href').get()
        next_page_absolute_url = response.urljoin(next_page_link)
        print('next page absolute url: ', next_page_absolute_url)

        # if self.page_count < 5:
        #     self.page_count += 1
        yield scrapy.Request(url=next_page_absolute_url, callback=self.parse)



# "form_number": "Form W-2",
# "form_title": "Wage and Tax Statement (Info Copy Only)",
# "min_year": 1954,
# "max_year": 2021



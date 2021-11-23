# py-scraper-crawler

## Using Python and Scrapy for web crawling/scraping

Python version: 3.10.0
Scrapy version: 2.5.1

From inside the project directory `irs_forms`, run this command to install dependencies:
`python3 -m pip install -r requirements.txt`

There are two utilities: `irsforms` and `downloadforms` for scraping IRS forms data from the [IRS Prior Year Products](https://apps.irs.gov/app/picklist/list/priorFormPublication.html) website.

To run each from the command line, from inside the project directory, the commands are:

`scrapy crawl irsforms`


`scrapy crawl downloadforms`

Each utility will prompt for user input from the command line.

`irsforms` prompts 'Enter form name(s) separated by commas, ie. W-2,1040,1099-A'.

`downloadforms` prompts 'Enter a form number, a comma, and a year or range of years, ie. W-2,1995-2000'.

Once you have provided proper input at the prompt, the corresponding utility will scrape and crawl the site to get the requested results, which will be written to the `irs_forms/results` folder. This folder will be created if it does not exist.

`irsforms` creates a JSON-formatted file named `form_info.json`.

`downloadforms` creates a separate folder for each form downloaded, named after the form, ie `Form W-2`. Inside the folder are the downloaded PDF files for the specified years for which the form is available.

## The files used and modifed from the Scrapy default for this project are as follows:

Spiders
- irsforms.py: scrapes the site for forms that match the input criteria
- downloadforms.py: scrapes the site for forms and download links that match the input criteria

Pipelines

In the pipelines.py file, two pipeline classes are defined:
- IrsFormsPipeline: processes items returned from the irsforms spider and writes to a text file in JSON format
- DownloadFormsPipeline: processes items returned from the downloadforms spider and downloads linked PDFs to a custom named directory/file structure

Settings
- settings.py: used to enable item pipelines and to set custom parameters to make sure each spider is connected only to its corresponding pipeline for item processing
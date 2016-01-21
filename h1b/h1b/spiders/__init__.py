# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import scrapy
from scrapy.http import FormRequest
from scrapy import optional_features
optional_features.remove('boto')

import pandas as pd


class H1BSpider(scrapy.Spider):
    name = "h1b"
    allowed_domains = ["h1bdata.info"]
    start_urls = [
        "http://h1bdata.info/",
    ]

    def __init__(self, employer='', job='', city='', *args, **kwargs):
        super(H1BSpider, self).__init__(*args, **kwargs)
        self.employer = employer
        self.job = job
        self.city = city

    def parse(self, response):
        formdata = {'em': self.employer, 'job': self.job, 'city': self.city}
        yield FormRequest.from_response(response,
                                        formdata=formdata,
                                        # clickdata={'name': 'commit'},
                                        callback=self.parse2)

    def parse2(self, response):
        filename = ''.join([self.employer, self.job, self.city])
        df = pd.read_html(response.body)[0]
        df.to_csv(filename+'.csv', index=False)
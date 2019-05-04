# -*- coding: utf-8 -*-
import os
import scrapy
import pandas as pd 

dir_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


df = pd.read_csv(filepath_or_buffer=dir_path+'/tripadvisor_all_location.csv')

# alter index to get other location
identify_link = list(df.identify_link)[23]
link = list(df.link)[23]


class TripadvisorHotelSpider(scrapy.Spider):
    name = 'tripadvisor_hotel'
    allowed_domains = ['tripadvisor.com.vn']
    start_urls = [link]

    custom_settings={ 'FEED_URI': f"tripadvisor_{identify_link}.csv",
                       'FEED_FORMAT': 'csv'}


    def parse(self, response):

        print("procesing:"+response.url)
        
        hotel_class=response.css(".listing_title > a")
        name_hotel=hotel_class.css("a::text").extract()
        url_hotel=hotel_class.css("a::attr(href)").extract()

        row_data=zip(name_hotel, url_hotel)

        for item in row_data:
            scraped_info = {
                'name_hotel':item[0],
                'url' : response.urljoin(item[1])
            }

            yield scraped_info


        NEXT_PAGE_SELECTOR = ".ui_pagination > a.next::attr(href)"
        next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
        if next_page:
            yield scrapy.Request(
            response.urljoin(next_page),
            callback=self.parse)

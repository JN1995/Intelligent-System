# -*- coding: utf-8 -*-
import scrapy


class TripadvisorVietnamSpider(scrapy.Spider):
    name = 'tripadvisor_VietNam'
    allowed_domains = ['tripadvisor.com.vn']
    start_urls = ['https://www.tripadvisor.com.vn/']

    custom_settings={ 'FEED_URI': "tripadvisor_all_location.csv",
                       'FEED_FORMAT': 'csv'}

    def parse(self, response):
        print("procesing:"+response.url)
        
        LOCATION_SELECTOR = "div.customSelection > div.boxhp.collapsibleLists > div.section > div.ui_columns > ul > li > a" 
        location_hotels = response.css(LOCATION_SELECTOR)

        name_location = location_hotels.css("a::text").extract()
        links = location_hotels.css("a::attr(href)").extract()

        identify_links = [link.split("-")[2] for link in links]
        row_data=zip(name_location, identify_links, links)

        #Making extracted data row wise,
        for item in row_data:
            #create a dictionary to store the scraped info
            scraped_info = {
                #key:value
                'name_location':item[0],
                'identify_link' : item[1],
                'link': response.urljoin(item[2]),
            }

            #yield or give the scraped info to scrapy
            yield scraped_info

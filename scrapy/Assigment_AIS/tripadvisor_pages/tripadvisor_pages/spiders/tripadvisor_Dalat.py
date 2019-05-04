# -*- coding: utf-8 -*-
import scrapy


class TripadvisorDalatSpider(scrapy.Spider):
    name = 'tripadvisor_Dalat'
    allowed_domains = ['tripadvisor.com.vn']
    start_urls = ['https://www.tripadvisor.com.vn/Hotels-g293922-Da_Lat_Lam_Dong_Province-Hotels.html/']

    custom_settings={ 'FEED_URI': "tripadvisor_DaLat.csv",
                       'FEED_FORMAT': 'csv'}

    def parse(self, response):

        print("procesing:"+response.url)
        
        hotel_class=response.css(".listing_title > a")
        name_hotel=hotel_class.css("a::text").extract()
        url_hotel=hotel_class.css("a::attr(href)").extract()

        row_data=zip(name_hotel, url_hotel)

        #Making extracted data row wise
        for item in row_data:
            #create a dictionary to store the scraped info
            scraped_info = {
                #key:value
                'name_hotel':item[0],
                'url' : response.urljoin(item[1])
            }

            #yield or give the scraped info to scrapy
            yield scraped_info


        NEXT_PAGE_SELECTOR = ".ui_pagination > a.next::attr(href)"
        next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
        if next_page:
            yield scrapy.Request(
            response.urljoin(next_page),
            callback=self.parse)

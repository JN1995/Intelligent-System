# -*- coding: utf-8 -*-

import os
import scrapy
import pandas as pd 

dir_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

df = pd.read_csv(filepath_or_buffer=dir_path+'/tripadvisor_all_location.csv')

# alter index to get other location
identify_link = list(df.identify_link)[23]

df = pd.read_csv(filepath_or_buffer=dir_path+f"/tripadvisor_{identify_link}.csv")

name_hotels = list(df.name_hotel)
urls = list(df.url)

# a = df.loc[df['url'] == urls[0]]["name_hotel"][0]
# print(a)

# print(name_hotels)


class TripadvisorHotelCommentSpider(scrapy.Spider):
    name = 'tripadvisor_hotel_comment'
    allowed_domains = ['tripadvisor.com.vn']
    start_urls = urls

    custom_settings={ 'FEED_URI': f"tripadvisor_comment_{identify_link}.csv",
                       'FEED_FORMAT': 'csv'}
    
    print(len(start_urls))

    def parse(self, response):
        print("procesing:"+response.url)

        COMMENT_SELECTOR = "div.hotels-review-list-parts-SingleReview__reviewContainer--d54T4"

        AUTHOR_COMMENT_SELECTOR = """div.hotels-review-list-parts-ReviewCardHeader__padding--R2JnR > 
        div.social-member-event-MemberEventOnObjectBlock__member_event_block--1Kusx > 
        div.social-member-event-MemberEventOnObjectBlock__event_wrap--1YkeG > 
        div.social-member-event-MemberEventOnObjectBlock__event_type--3njyv > 
        span > 
        a"""
        
        LINK_CONTENT_COMMENT_SELECTOR = """div.hotels-review-list-parts-SingleReview__mainCol--2XgHm > 
        div.hotels-review-list-parts-ReviewTitle__reviewTitle--2Fauz > 
        a::attr(href)"""
        
        comment = response.css(COMMENT_SELECTOR)
        author_comment = comment.css(AUTHOR_COMMENT_SELECTOR)
        link_content_comments = comment.css(LINK_CONTENT_COMMENT_SELECTOR).extract()

        username_author = author_comment.css("a::text").extract()
        link_username_author = author_comment.css("a::attr(href)").extract()

        row_data=zip(username_author, link_username_author, link_content_comments)

        #Making extracted data row wise
        for item in row_data:
            #create a dictionary to store the scraped info
            scraped_info = {
                'username_author':item[0],
                'link_username_author' : response.urljoin(item[1]),
                "link_content_comment": response.urljoin(item[2]),
            }

            #yield or give the scraped info to scrapy
            yield scraped_info


        NEXT_PAGE_SELECTOR = ".ui_pagination > a.next::attr(href)"
        next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
        if next_page:
            yield scrapy.Request(
            response.urljoin(next_page),
            callback=self.parse)

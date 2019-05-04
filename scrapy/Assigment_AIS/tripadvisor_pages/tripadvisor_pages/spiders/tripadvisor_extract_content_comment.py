# -*- coding: utf-8 -*-
import os
import scrapy
import pandas as pd 

RATING = {
    "ui_bubble_rating bubble_50": "5",
    "ui_bubble_rating bubble_40": "4",
    "ui_bubble_rating bubble_30": "3",
    "ui_bubble_rating bubble_20": "2",
    "ui_bubble_rating bubble_10": "1"
}

dir_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

df = pd.read_csv(filepath_or_buffer=dir_path+'/tripadvisor_all_location.csv')

# alter index to get other location
identify_link = list(df.identify_link)[23]

df = pd.read_csv(filepath_or_buffer=dir_path+f"/tripadvisor_comment_{identify_link}.csv")

username_authors = list(df.username_author)
link_content_comments = list(df.link_content_comment)


class TripadvisorExtractContentCommentSpider(scrapy.Spider):
    name = 'tripadvisor_extract_content_comment'
    allowed_domains = ['tripadvisor.com.vn']
    start_urls = link_content_comments

    custom_settings={ 'FEED_URI': f"tripadvisor_content_comment_{identify_link}.csv",
                       'FEED_FORMAT': 'csv'}

    print(len(start_urls))

    def parse(self, response):
        print("procesing:"+response.url)

        COMMENT_SELECTOR = "div.prw_rup.prw_reviews_resp_sur_h_featured_review"

        HOTEL_NAME_SELECTOR = "div.altHeadInline > a::text"

        RATING_SELECTOR = "span.ui_bubble_rating::attr(class)"

        CONTENT_COMMENT_SELECTOR = "div.prw_rup.prw_reviews_resp_sur_review_text > div.entry > p.partial_entry > span.fullText::text"
        
        STAY_DATE_SELECTOR = "div.prw_rup.prw_reviews_stay_date_hsx::text"

        TRIP_CATEGORY_SELECTOR = "div.prw_rup.prw_reviews_category_ratings_hsx > div > div > div::text"
        
        comment = response.css(COMMENT_SELECTOR)

        scraped_info = {
            "name_author_comment": username_authors[link_content_comments.index(response.url)],
            "name_hotel": comment.css(HOTEL_NAME_SELECTOR).extract_first() ,
            "rating": RATING[comment.css(RATING_SELECTOR).extract_first()],
            "content_comments": comment.css(CONTENT_COMMENT_SELECTOR).extract(),
            "stay_date": comment.css(STAY_DATE_SELECTOR).extract_first() ,
            "trip_category": comment.css(TRIP_CATEGORY_SELECTOR).extract_first(),
        }

        yield scraped_info

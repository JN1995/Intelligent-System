# -*- coding: utf-8 -*-
import scrapy

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from hotel.items import HotelItem

CLASS_COMMENT = ".hotels-hotel-review-community-content-review-list-parts-SingleReview__reviewContainer--2LYmA"
CLASS_USER_COMMENT = "hotels-hotel-review-community-content-review-list-parts-ReviewCardHeader__padding--1pnnR"


class HotelVietnamSpider(CrawlSpider):
    name = "hotel_vietnam"
    allowed_domains = ["www.tripadvisor.com.vn"]
    start_urls = (
        "https://www.tripadvisor.com.vn/Hotel_Review-g293922-d7735715-Reviews-Terracotta_Hotel_Resort-Da_Lat_Lam_Dong_Province/",
    )

    rules = (
        Rule(
            LinkExtractor(allow=(), restrict_css=(".next",)),
            callback="parse_item",
            follow=False,
        ),
    )


    def parse_item(self, response):
        print("================parse_item================")
        print("processing ...", response.url)
        item_comment = response.css(
            ".hotels-hotel-review-community-content-review-list-parts-ReviewCardHeader__padding--1pnnR > \
                .social-member-MemberEventOnObjectBlock__member_event_block--2byME"
        )

        # item_links = response.css('.large > .detailsLink::attr(href)').extract()
        # for a in item_links:
        #     yield scrapy.Request(a, callback=self.parse_detail_page)
        href = item_comment.css(".inline::attr(href)").extract()
        for h in href:
            print(h)

    #     print("jjjjjjjjjjjj")
    #     title = response.css('h1::text').extract()[0].strip()
    #     price = response.css('.pricelabel > strong::text').extract()[0]

    #     item = HotelItem()
    #     item['title'] = title
    #     item['price'] = price
    #     item['url'] = response.url
    #     yield item

    parse_start_url = parse_item

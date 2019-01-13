# -*- coding: utf-8 -*-
import scrapy
from reddit_yt.items import RedditYtItem


class RedditYtLinksSpider(scrapy.Spider):
    name = 'reddit-yt-links'
    # allowed_domains = ['http://www.reddit.com/r/videos/']
    start_urls = ['http://www.reddit.com/r/videos/']

    def parse(self, response):
        for post in response.xpath('//div[contains(@class, "Post")]'):
            reddit_link = 'https://www.reddit.com{}'.format(
                post.xpath('.//a[starts-with(@href, "/r/videos/comments/")]/@href').extract_first()
            )

            yield RedditYtItem(
                title=post.xpath('.//h2/text()').extract_first(),
                link=post.xpath('.//a[contains(@href, "youtu")]/@href').extract_first(),
                reddit_link=reddit_link,
            )
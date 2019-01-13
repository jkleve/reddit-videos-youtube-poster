# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
# from queue import Queue
from scrapy.exceptions import DropItem

from models import db, NewPost


class RedditYtPipeline(object):

    def __init__(self):
        self.links = set()

    def process_item(self, item, spider):
        if item['link']:
            if NewPost.get_or_none(NewPost.link == item['link']):
                raise DropItem('Post already in database')
            post = NewPost(title=item['title'], link=item['link'], reddit_link=item['reddit_link'])
            post.save()
            return item
        else:
            raise DropItem('Missing link')

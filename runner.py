import sys

from datetime import datetime, timedelta
from googleapiclient.errors import HttpError
from logging import getLogger
from logging.config import dictConfig
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from models import db, NewPost, Post
from settings import *
from reddit_yt.spiders import RedditYtLinksSpider
from youtube import (
    get_authenticated_service,
    YoutubePlaylist,
    YoutubeVideo,
    video_id_regex,
    video_id_regex_short
)

log = getLogger(__name__)

logging_config = {
    'version': 1,
    'formatters': {
        'brief': {
            'format': '%(asctime)s %(levelname)-8s %(name)s: %(message)s',
            'datefmt': '%H:%M:%S',
        },
    },
    'handlers': {
        'brief': {
            'class': 'logging.StreamHandler',
            'formatter': 'brief',
            'stream': 'ext://sys.stdout',
        },
    },
    'loggers': {
        '__main__': {
            'level': 'DEBUG',
            'handlers': ('brief',),
        },
    },
}

dictConfig(logging_config)


def remove_old_from_db(model, date):
    """Remove anything older than date from database"""
    q = model.delete().where(model.created_date < date)
    q.execute()


def delete_all(model):
    q = model.delete()
    q.execute()


def list_all(model):
    q = model.select()
    for p in q:
        print('{:20}: {}'.format(p.title, p.link))


def post_videos(client, playlist):
    for new_post in NewPost.select():
        if not Post.get_or_none(Post.link == new_post.link):
            video_id = get_video_id(new_post.link)

            if video_id:
                log.debug('Adding video {} to {}'.format(video_id, playlist))

                # add to playlist
                playlist.add(video_id)

                # comment on video
                video = YoutubeVideo(client, video_id)
                comment = YOUTUBE_COMMENT_TEMPLATE.format(title=new_post.title, link=new_post.reddit_link)
                try:
                    video.comment_thread(YOUTUBE_CHANNEL_ID, comment)
                except HttpError:
                    log.warning('Failed to post comment to {}'.format(new_post.link))

                # save to database
                Post.create(title=new_post.title, link=new_post.link,
                    reddit_link=new_post.reddit_link, created_date=new_post.created_date)
            else:
                log.warning('Failed to get video ID of {}'.format(new_post.link))
        else:
            log.debug('Video {} already posted'.format(new_post.link))

        if DEBUG:  # only do one case in debug
            break


def get_video_id(link):
    """Return the Youtube video ID given a youtube video link"""
    match = video_id_regex.search(link)
    if match:
        return match.group(1)

    match = video_id_regex_short.search(link)
    if match:
        return match.group(1)


def crawl(spider):
    """Runs the web crawler"""
    process = CrawlerProcess(get_project_settings())

    process.crawl(spider)
    process.start()


def main():
    client = get_authenticated_service()
    playlist = YoutubePlaylist(client, YOUTUBE_PLAYLIST_ID)

    db.connect()

    if not db.table_exists(DB_TABLE_NEW_POSTS_NAME):
        db.create_tables([NewPost,])
    if not db.table_exists(DB_TABLE_POSTS_NAME):
        db.create_tables([Post,])
    else:
        remove_old_from_db(Post, datetime.now() - timedelta(**DB_POST_KEEP_DURATION))

    delete_all(NewPost)
    crawl(RedditYtLinksSpider)

    post_videos(client, playlist)

    db.close()


if __name__ == '__main__':
    sys.exit(main())

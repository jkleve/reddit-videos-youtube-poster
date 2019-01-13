# Database
DB_NAME = 'posts.db'
DB_TABLE_POSTS_NAME = 'top_of_rvideos'
DB_TABLE_NEW_POSTS_NAME = 'top_of_rvideos_new'
# This can contain anything a datetime.timedelta object can take on construction
# https://docs.python.org/3/library/datetime.html#datetime.timedelta
DB_POST_KEEP_DURATION = {
    'days': 2,
}

# Youtube
YOUTUBE_CHANNEL_ID = 'UCxYglkYGjvKUhfWdVvHvXcg'
YOUTUBE_PLAYLIST_ID = 'PL_3yUKBsaMOxCDcm2yt0Q1nHTnAYgTAAq'
YOUTUBE_COMMENT_TEMPLATE = """
{title}

{link}
"""
from datetime import datetime
from peewee import CharField, DateTimeField, Model, SqliteDatabase

from settings import *

db = SqliteDatabase(DB_NAME)


class NewPost(Model):
    title = CharField()
    link = CharField()
    reddit_link = CharField()
    created_date = DateTimeField(default=datetime.now)

    class Meta:
        database = db
        table_name = DB_TABLE_NEW_POSTS_NAME


class Post(Model):
    title = CharField()
    link = CharField()
    reddit_link = CharField()
    created_date = DateTimeField()

    class Meta:
        database = db
        table_name = DB_TABLE_POSTS_NAME
import httplib2
import os
import sys

from apiclient.discovery import build_from_document
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

CLIENT_SECRETS_FILE = 'client_secrets.json'
YOUTUBE_READ_WRITE_SSL_SCOPE = "https://www.googleapis.com/auth/youtube.force-ssl"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:
   %s
with information from the APIs Console
https://console.developers.google.com

For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   CLIENT_SECRETS_FILE))


def get_authenticated_service():
    flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, scope=YOUTUBE_READ_WRITE_SSL_SCOPE,
        message=MISSING_CLIENT_SECRETS_MESSAGE)

    storage = Storage("%s-oauth2.json" % sys.argv[0])
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        raise Exception('shit.. fix this.')
        # credentials = run_flow(flow, storage, args)

    # Trusted testers can download this discovery document from the developers page
    # and it should be in the same directory with the code.
    with open("youtube-v3-discoverydocument.json", "r") as f:
        doc = f.read()
        return build_from_document(doc, http=credentials.authorize(httplib2.Http()))


class YoutubePlaylist(object):
    def __init__(self, client, playlist_id):
        self._client = client
        self._playlist_id = playlist_id

    def add(self, video_id):
        result = self._client.playlistItems().insert(
            part="snippet",
            body=dict(
                snippet=dict(
                    playlistId=self._playlist_id,
                    resourceId=dict(
                        kind='youtube#video',
                        videoId=video_id,
                    ),
                )
            )
        ).execute()

    def __repr__(self):
        return 'YoutubePlaylist({})'.format(self._playlist_id)


class YoutubeVideo(object):
    def __init__(self, client, video_id):
        self._client = client
        self._video_id = video_id

    def comment_thread(self, channel_id, text):
        result = self._client.commentThreads().insert(
            part="snippet",
            body=dict(
                snippet=dict(
                    channelId=channel_id,
                    videoId=self._video_id,
                    topLevelComment=dict(
                        snippet=dict(
                            textOriginal=text,
                        ),
                    ),
                ),
            )
        ).execute()


if __name__ == '__main__':
    # TODO test both methods
    video_id = 'NRZZ7kpdGvo'
    playlist_id = 'PL_3yUKBsaMOxCDcm2yt0Q1nHTnAYgTAAq'
    client = get_authenticated_service()
    playlist = YoutubePlaylist(client, playlist_id)
    playlist.add(video_id)

import json

from tweepy.streaming import StreamListener
from tweepy import Stream, OAuthHandler
import couchdb

import settings

class CouchDBStreamListener(StreamListener):
    def __init__(self, db):
        self.db = db
        self.tweet_count = 0
        self.received_friend_ids = False

    def on_data(self, data):
        try:
            tweet = json.loads(data)
        except Exception:
            print("Failed to parse tweet data")
            tweet = None

        if tweet:
            if tweet.has_key('id') and tweet.has_key("text"):
                print("%s: %s" % (tweet['user']['screen_name'], tweet['text']))

                tweet['doc_type'] = "tweet"

                self.db["tweet:%d" % tweet['id']] = tweet

                self.tweet_count += 1
            elif not self.received_friend_ids and tweet.has_key("friends"):
                print("Got %d user ids" % len(tweet['friends']))
                self.received_friend_ids = True
            else:
                print("Received a responce that is not a tweet")
                print tweet

        return True

def main():
    auth = OAuthHandler(settings.consumer_key, 
                        settings.consumer_secret)

    auth.set_access_token(settings.access_token, 
                          settings.access_secret)

    server = couchdb.Server()
    db = server[settings.database]

    listener = CouchDBStreamListener(db)

    stream = Stream(auth, listener)
    
    try:
        stream.userstream()
    except KeyboardInterrupt:
        print("Total tweets received: %d" % listener.tweet_count)

if __name__ == "__main__":
    main()

import tweepy
import configparser
import random
import time

# reading data from config file

config = configparser.ConfigParser()
config.read("./config.ini")

latest_tweet = config["TWEETS"]["last"]

consumer_key = config["API"]["CONSUMER_KEY"]
consumer_secret = config["API"]["CONSUMER_SECRET"]
access_token = config["API"]["ACCESS_KEY"]
access_secret = config["API"]["ACCESS_SECRET"]

# authentication + initialization
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

# search for tweets under hashtags

if latest_tweet != "placeholder":
    tweets = [tweet for tweet in tweepy.Cursor(api.search_tweets, q="#Hedera", result_type="recent", since_id=int(latest_tweet)).items(100)]
else:
    tweets = [tweet for tweet in tweepy.Cursor(api.search_tweets, q="#Hedera", result_type="recent").items(100)]

# write the last tweet so it doesn't reply to the same thing twice

latest_tweet = tweets[0].id

config.set("TWEETS", "last", str(latest_tweet))

with open('./config.ini', 'w') as configfile:
    config.write(configfile)

# pick a phrase and reply to tweets with media

ids = []
for tweet in tweets:
    media = api.media_upload(filename="./giphy.gif")
    phrase = random.choice(config["PHRASES"]["phrases"].split(", "))
    api.update_status(status = phrase, in_reply_to_status_id = str(tweet.id), auto_populate_reply_metadata=True, media_ids=[media.media_id])
    time.sleep(600)


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
    tweets = [tweet for tweet in tweepy.Cursor(api.search_tweets, q="#Hedera", result_type="recent", since_id=int(latest_tweet)).items(500)]
else:
    tweets = [tweet for tweet in tweepy.Cursor(api.search_tweets, q="#Hedera", result_type="recent").items(100)]


latest_tweet = tweets[0].id

config.set("TWEETS", "last", str(latest_tweet))

with open('./config.ini', 'w') as configfile:
    config.write(configfile)

# pick a phrase
# reply to tweets
for tweet in tweets:
    phrase = random.choice(config["PHRASES"]["phrases"].split(", "))
    x = tweet.id
    api.update_status_with_media(status=phrase, filename="./giphy.gif", in_reply_to_status_id = x)
    time.sleep(120)


import tweepy
import configparser
import random
import time
from os import listdir
import os

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

print("[+] Connected to API")

# search for tweets under hashtags

print("[/] Retrieving tweets...")

tweets = []

if latest_tweet != "placeholder":
    for term in config["PHRASES"]["terms"].split(", "):
        tweets += [tweet for tweet in tweepy.Cursor(api.search_tweets, q=term, result_type="recent", since_id=int(latest_tweet)).items(100)]
else:
    for term in config["PHRASES"]["terms"].split(", "):
        tweets += [tweet for tweet in tweepy.Cursor(api.search_tweets, q=term, result_type="recent").items(100)]
print("[+] tweets recieved")

# write the last tweet so it doesn't reply to the same thing twice

latest_tweet = tweets[0].id

config.set("TWEETS", "last", str(latest_tweet))

with open('./config.ini', 'w') as configfile:
    config.write(configfile)

# pick a random gif
src = os.path.join((os.path.join(os.getcwd(), "src")), random.choice(listdir("src")))


# pick a phrase and reply to tweets with media

for tweet in tweets:
    print("[/] Tweeting...")
    media = api.media_upload(filename=src)
    phrase = random.choice(config["PHRASES"]["phrases"].split(", "))
    api.update_status(status = phrase, in_reply_to_status_id = str(tweet.id), auto_populate_reply_metadata=True, media_ids=[media.media_id])
    print("[+] Tweeted and waiting 10 minutes")
    time.sleep(6000)


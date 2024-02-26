from keys import consumer_key, consumer_secret, access_token, access_token_secret
import tweepy

# Authenticate Twitter/X Account

def authenticate_twitter():
    return tweepy.Client(consumer_key=consumer_key,consumer_secret=consumer_secret,access_token=access_token,access_token_secret=access_token_secret)

# Post Tweet from Account

def post_tweet(client, tweet_text):
    try:
        client.create_tweet(text=tweet_text)
    except tweepy.TweepyException as e:
        print(e)
from keys import bearer_token, consumer_key, consumer_secret, access_token, access_token_secret
import tweepy

# Authenticate Twitter/X Account

def authenticate_twitter():
    return tweepy.Client(bearer_token, consumer_key, consumer_secret, access_token, access_token_secret)

# Reply to a Tweet

def reply_tweet(client, tweet_id, tweet_text):
    try:
        client.create_tweet(in_reply_to_tweet_id='1761967578896097405', text="replied")
    except tweepy.TweepyException as e:
        print(e)

# Direct Message Error

def direct_message(client, id):
    try:
        response = "I had an problem attempting to paint you an image. Please ensure that the tweet is valid and adheres to the guidelines. Please try again later.\n\n- PictureThatBot"
        client.create_direct_message(participant_id=id, text=response)
    except tweepy.TweepyException as e:
        print(e)
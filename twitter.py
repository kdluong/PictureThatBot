from keys import bearer_token, consumer_key, consumer_secret, access_token, access_token_secret
import tweepy

# Authenticate Twitter/X Account

def getApi():
    auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
    return tweepy.API(auth)

def getClient():
    return tweepy.Client(bearer_token, consumer_key, consumer_secret, access_token, access_token_secret)

# Reply to a Tweet

def reply_tweet(client, tweet_id, media_id):
    try:
        client.create_tweet(in_reply_to_tweet_id=tweet_id, media_ids=[media_id])
    except tweepy.TweepyException as e:
        print(e)

# Direct Message Error

def direct_message(client, id):
    try:
        response = """
            I encountered a little hiccup while fluttering my artistic feathers to craft an image for you. 
            Kindly ensure that your tweet is chirp-worthy and aligns with our artistic guidelines. 
            Feel free to give it another go, and I'll be back to paint your vision in a tweet-worthy masterpiece. 
            Thank you for your patience!
            
            \n\n- PictureThatBot
        """
        client.create_direct_message(participant_id=id, text=response)
    except tweepy.TweepyException as e:
        print(e)
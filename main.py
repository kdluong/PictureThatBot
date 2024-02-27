from twitter import getApi, getClient, reply_tweet, direct_message
from gpt4 import generateImage
import time

def mentionTweet(api, client, tweet):

    if tweet.referenced_tweets != None:
        original_tweet = client.get_tweet(tweet.referenced_tweets[0].id).data.text
        media = generateImage(api, original_tweet)
    else:
        media = generateImage(api, tweet.text)

    if media == 'fail':
        direct_message(client, tweet.author_id)
        print("Sent DM")
    else:
        reply_tweet(client, tweet.id, media.media_id)
        print("Tweeted")

def main():
    
    api = getApi()
    client = getClient()

    if api and client:

        client_id = client.get_me().data.id

        # start loop

        response = client.get_users_mentions(id=client_id, expansions=['author_id', 'referenced_tweets.id'])
        
        if response.data != None:

            for tweet in response.data:

                if tweet.id != 1761801546885439854:
                    mentionTweet(api, client, tweet)

        #         #time.sleep(3)
    
    else:
        print("Failed to authenticate with Twitter.")

if __name__ == "__main__":
    main()
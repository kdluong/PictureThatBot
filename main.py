from twitter import getApi, getClient, reply_tweet, direct_message
from gpt4 import generateImage
import time
from concurrent.futures import ThreadPoolExecutor
import concurrent
from datetime import datetime
import tweepy

def perform_operation(api_operation, *args, **kwargs):
    result = None

    while result == None:
        try:
            result = api_operation(*args, **kwargs)
        except tweepy.errors.TooManyRequests as e:

            waitTime = int(e.response.headers['x-rate-limit-reset'])
            current_timestamp = int(datetime.now().timestamp())
            time_remaining = max(waitTime - current_timestamp, 0)

            print(f"Too many requests, sleeping for {time_remaining} seconds...")
            time.sleep(time_remaining)
    
    return result

def replyToTweet(api, client, tweet):

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
        print("Sent Tweet")

def getLatestReply(client):

    response_params = {
        'max_results': 1,
        'expansions': ['referenced_tweets.id']
    }

    latestResponse = perform_operation(client.get_home_timeline, **response_params)

    start_id = None

    if latestResponse.data != None:
        if latestResponse.data[0].referenced_tweets != None:
            start_id = latestResponse.data[0].referenced_tweets[0].id
            print("1A of 3: Fetching Original Tweet")

            response_params = {
                'id': start_id,
                'tweet_fields': ['created_at']
            }

            original_tweet = perform_operation(client.get_tweet, **response_params)

            start_date = original_tweet.data.created_at.isoformat()
        else:
            start_date = latestResponse.data.created_at.isoformat()
    else:
        start_date = datetime.now().isoformat()

    return (start_id, start_date)

def fetchTweets(client):

    print("1 of 3: Fetching Latest Reply")
    
    latestTweet = getLatestReply(client)
    client_id = client.get_me().data.id
    
    print("2 of 3: Fetching Tweets")
    
    response_params = {
        'id': client_id,
        'expansions': ['author_id', 'referenced_tweets.id'],
        'start_time': latestTweet[1],
        'tweet_fields': ['created_at']
    }

    if latestTweet[0] != None:
        response_params['since_id'] = latestTweet[0]

    return perform_operation(client.get_users_mentions, ** response_params)

def main():
    
    api = getApi()
    client = getClient()

    if api and client:

        # start loop

        tweets = fetchTweets(client)

        print("3 of 3: Printing Tweets")
    
        if tweets.data != None:
      
            with ThreadPoolExecutor() as executor:
                
                # Submit each tweet processing task to the executor
                futures = [executor.submit(replyToTweet, api, client, tweet) for tweet in tweets.data]

                # Wait for all tasks to complete
                concurrent.futures.wait(futures)

        else:
            print("No Tweets Yet...")

        # sleep for 10min
        # end loop
    
    else:
        print("Failed to authenticate with Twitter.")

if __name__ == "__main__":
    main()
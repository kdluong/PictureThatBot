from datetime import datetime
from keys import *
import tweepy
import time

# Authenticate Twitter/X Account


def get_api():
    auth = tweepy.OAuth1UserHandler(
        consumer_key, consumer_secret, access_token, access_token_secret
    )
    return tweepy.API(auth)


def get_client():
    return tweepy.Client(
        bearer_token,
        consumer_key,
        consumer_secret,
        access_token,
        access_token_secret,
        wait_on_rate_limit=True,
    )


# Send Generated Image via Tweet


def send_tweet(client, tweet_id, media_id):

    response_params = {"in_reply_to_tweet_id": tweet_id, "media_ids": [media_id]}

    perform_tweepy_operation(client.create_tweet, **response_params)


# Send Error via Direct Message


def send_dm(client, id):

    response = """
            I encountered a little hiccup while fluttering my artistic feathers to craft an image for you. 
            Kindly ensure that your tweet is chirp-worthy and aligns with our artistic guidelines. 
            Feel free to give it another go, and I'll be back to paint your vision in a tweet-worthy masterpiece. 
            Thank you for your patience!
            
            \n\n- PictureThatBot
        """

    response_params = {"participant_id": id, "text": response}

    perform_tweepy_operation(client.create_direct_message, **response_params)


# Execute Tweepy Operation w/ Error Handling


def perform_tweepy_operation(api_operation, *args, **kwargs):

    result = None

    # Attempt to perform operation

    while result == None:
        try:
            result = api_operation(*args, **kwargs)
        except tweepy.errors.TooManyRequests as e:

            # Handle Too Many Requests

            # Fetch wait time

            waitTime = int(e.response.headers["x-rate-limit-reset"])
            current_timestamp = int(datetime.now().timestamp())
            time_remaining = max(waitTime - current_timestamp, 0)

            # Sleep until wait time is over

            print(f"Too many requests, sleeping for {time_remaining} seconds...")
            time.sleep(time_remaining)

        except tweepy.errors.TweepyException as e:

            # Handle other Tweepy-related errors

            print(f"A Tweepy error occurred: \n\n{e}\n\n")

        except Exception as e:

            # Handle any other exceptions

            print(f"An unexpected error occurred: \n\n{e}\n\n")

    return result


# Fetch Recent Mentioned Tweets


def fetch_tweets(client):

    # Fetch latest reply, to prevent duplicates

    print("1 of 3: Fetching Latest Reply")

    latestTweet = fetch_latest_tweet(client)
    client_id = client.get_me().data.id

    # Fetch tweets mentioning @picturethatbot

    print("2 of 3: Fetching Tweets")

    response_params = {
        "id": client_id,
        "expansions": ["author_id", "referenced_tweets.id"],
        "start_time": latestTweet[1],
        "tweet_fields": ["created_at"],
    }

    if latestTweet[0] != None:
        response_params["since_id"] = latestTweet[0]

    return perform_tweepy_operation(client.get_users_mentions, **response_params)


# Fetch Latest Processed Tweet


def fetch_latest_tweet(client):

    # Fetch latest proccessed tweet

    response_params = {"max_results": 1, "expansions": ["referenced_tweets.id"]}

    latestResponse = perform_tweepy_operation(
        client.get_home_timeline, **response_params
    )

    # Extract tweet's ID and date/time

    start_id = None

    if latestResponse.data != None:
        if latestResponse.data[0].referenced_tweets != None:
            start_id = latestResponse.data[0].referenced_tweets[0].id

            print("1A of 3: Fetching Original Tweet")

            response_params = {"id": start_id, "tweet_fields": ["created_at"]}

            original_tweet = perform_tweepy_operation(
                client.get_tweet, **response_params
            )

            start_date = original_tweet.data.created_at.isoformat()
        else:
            start_date = latestResponse.data.created_at.isoformat()
    else:
        start_date = datetime.now().isoformat()

    return (start_id, start_date)

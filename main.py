from concurrent.futures import ThreadPoolExecutor
from twitter import *
from gpt4 import generate_image
import concurrent

# Generate & Tweet Image


def process_tweet(api, client, tweet):

    # Generate an image based on tweet

    print("Generating Image...")

    if tweet.referenced_tweets != None:

        # if reply, find original tweet

        response_params = {"id": tweet.referenced_tweets[0].id}

        original_tweet = perform_tweepy_operation(client.get_tweet, **response_params)

        if original_tweet.errors != []:
            media = "failed"
        else:
            media = generate_image(api, original_tweet.data.text)
    else:
        media = generate_image(api, tweet.text)

    # Send Tweet/DM if Success/Fail

    if media == "failed":
        send_dm(client, tweet.author_id)
        print("Sent DM")
    else:
        send_tweet(client, tweet.id, media.media_id)

        print("Sent Tweet")


# Handle Multithreading


def handler(event, context):

    # Attempt to authenticate user

    api = get_api()
    client = get_client()

    if api.verify_credentials():

        # Fetch tweets to process

        tweets = fetch_tweets(client)

        # Determine if tweets list contain tweets

        if tweets.data != None:

            print("3 of 3: Generating Images")

            # Organize tweets into threads as appropriate

            batch_size = 5

            with ThreadPoolExecutor() as executor:
                for i in range(0, len(tweets.data), batch_size):
                    batch = tweets.data[i : i + batch_size]

                    futures = [
                        executor.submit(process_tweet, api, client, tweet)
                        for tweet in batch
                    ]

                    concurrent.futures.wait(futures)

                    print("Cooling down for 60 seconds...")
                    time.sleep(60)
        else:
            print("3 of 3: No tweets yet...")

    else:
        print("Failed to authenticate with Twitter.")


from concurrent.futures import ThreadPoolExecutor
from gpt4 import generateImage
from twitter import *
import concurrent

# Generate & Tweet Image


def process_tweet(api, client, tweet):

    # Generate an image based on tweet

    if tweet.referenced_tweets != None:

        # if reply, find original tweet

        response_params = {"id": tweet.referenced_tweets[0].id}

        original_tweet = perform_tweepy_operation(client.get_tweet, **response_params)

        if original_tweet.errors != []:
            media = "failed"
        else:
            media = generateImage(api, original_tweet.data.text)
    else:
        media = generateImage(api, tweet.text)

    # Send Tweet/DM if Success/Fail

    if media == "failed":
        send_dm(client, tweet.author_id)
        print("Sent DM")
    else:
        send_tweet(client, tweet.id, media.media_id)
        print("Sent Tweet")


# Handle Multithreading


def main():

    # Attempt to authenticate user

    api = get_api()
    client = get_client()

    if api.verify_credentials():

        # Fetch tweets to process

        tweets = fetch_tweets(client)

        print("3 of 3: Generating Images")

        # Determine if tweets list contain tweets

        if tweets.data != None:

            # Organize tweets into threads as appropriate

            with ThreadPoolExecutor() as executor:
                futures = [
                    executor.submit(process_tweet, api, client, tweet)
                    for tweet in tweets.data
                ]
                concurrent.futures.wait(futures)
        else:
            print("No Tweets Yet...")

    else:
        print("Failed to authenticate with Twitter.")


if __name__ == "__main__":
    main()

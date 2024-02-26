from twitter import authenticate_twitter, post_tweet
from gpt4 import generateImage
    
def main():

    client = authenticate_twitter()
    
    # check user validity

    if client:

        # Post Tweet

            #tweet_text = "TEST TWEET2!"
            #post_tweet(client, tweet_text)

        # Generate Image

            # url = generateImage("Man running on water.")
            # print(url)

        print("Hello world")

    else:
        print("Failed to authenticate with Twitter.")

if __name__ == "__main__":
    main()
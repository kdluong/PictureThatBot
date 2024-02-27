from twitter import authenticate_twitter, reply_tweet, direct_message
from gpt4 import generateImage

# def orginalTweet():

# def mentionTweet():

def main():

    client = authenticate_twitter()

    if client:
        
        client_id = client.get_me().data.id

        response = client.get_users_mentions(id=client_id, expansions=['author_id', 'referenced_tweets.id'])
        
        if response.data != None:

            for tweet in response.data:

                if tweet.referenced_tweets != None:
                    for rt in tweet.referenced_tweets:
                        print("responded to:")
                        print(client.get_tweet(rt.id))
                else:
                    print("Original Tweet")
    
    else:
        print("Failed to authenticate with Twitter.")

if __name__ == "__main__":
    main()
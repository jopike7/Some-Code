import re
from Tkinter import *
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
 
### Twitter class for sentiment analysis of Aspyr Media videogame laucnh windows ###

class TwitterClient(object):

    def __init__(self):

        # keys and tokens from the Twitter Dev Console
        consumer_key = 'ZQ8Bo1dLWtcoxop7nhIewAglm'
        consumer_secret = '8KLeqsyxk37SNvxGXq46CLdvl5JOf8MFiS94odVeZWcLUTTPjQ'
        access_token = '3362105774-QV1qIOsKKXdt6i2RATzXITaulmtsM8N4NNBzaAp'
        access_token_secret = 'HkSiwmnMjHH1mbOCfE3WMggchpTP4BVrzRgodVjFhudnu'
 
        # attempt authentication
        try:
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            self.auth.set_access_token(access_token, access_token_secret)
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")
 
    def clean_tweet(self, tweet):
    
        # Utility function to clean tweet text by removing links, special characters using regex
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
 
    def get_tweet_sentiment(self, tweet):
        
        analysis = TextBlob(self.clean_tweet(tweet))
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'
 
    def get_tweets(self, query, count = 10):
        tweets = []
 
        try:
            fetched_tweets = self.api.search(q = query, count = count)
 
            for tweet in fetched_tweets:
                parsed_tweet = {}
 
                parsed_tweet['text'] = tweet.text
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)
 
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
                    
            return tweets
 
        except tweepy.TweepError as e:
            print("Error : " + str(e))
 
def main():

    api = TwitterClient()
    response = raw_input('What would you like to search? ')
    tweets = api.get_tweets(query = response, count = 400)
 
    # picking positive tweets from tweets
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    # percentage of positive tweets
    print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets)))
    # picking negative tweets from tweets
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    # percentage of neutral tweets
    print("Neutral tweets percentage: {} %".format(100*(len(tweets)-len(ntweets)-len(ptweets))/len(tweets)))
    # percentage of negative tweets
    print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets)))
 
    # printing first 5 positive tweets
    print("\n\nPositive tweets:")
    for tweet in ptweets[:10]:
        print(tweet['text'])
 
    # printing first 5 negative tweets
    print("\n\nNegative tweets:")
    for tweet in ntweets[:10]:
        print(tweet['text'])
 
if __name__ == "__main__":
    # calling main function
    main()

from textblob import TextBlob 
from dotenv import load_dotenv
import tweepy 
import os
from pathlib import Path

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

class TextBlobSen:
    def __init__(self, query):
        self.query = query

    def stream(self):
        C_KEY = os.getenv('C_KEY')
        C_SECRET = os.getenv('C_SECRET')
        A_TOKEN = os.getenv('A_TOKEN')
        A_SECRET = os.getenv('A_SECRET')

        auth_handler = tweepy.OAuthHandler(consumer_key=C_KEY, consumer_secret=C_SECRET)
        auth_handler.set_access_token(A_TOKEN, A_SECRET)

        api = tweepy.API(auth_handler)
    
        tweet_num = 200
        tweets = tweepy.Cursor(api.search, q=self.query, lang='en').items(tweet_num)

        return tweets


    def trim(self, char_to_trim, tweet):
        index = tweet.index(char_to_trim)
        final_tweet = tweet[index + 2:]

    def get_sentiment(self, tweets):
        polarity = 0
        positive = 0
        negative = 0
        neutral = 0
    
        for tweet in tweets:
            trimmed_tweet = tweet.text.replace('RT', '')

            if trimmed_tweet.startswith(' @'): self.trim(':', trimmed_tweet)
            if trimmed_tweet.startswith('@'): self.trim(' ', trimmed_tweet)
            
            sentiment = TextBlob(trimmed_tweet)

            if sentiment.polarity > 0: positive += 1
            elif sentiment.polarity < 0: negative += 1
            elif sentiment.polarity == 0: neutral += 1

            polarity += sentiment.polarity

        return polarity, positive, negative, neutral

    def analyise(self):
        streamed_tweets = self.stream()
        polarity, positive, negative, neutral = self.get_sentiment(streamed_tweets)
        
        print(f'Analysis for {self.query}')
        print(f'positive tweets => {positive}')
        print(f'neutral tweets => {neutral}')
        print(f'negative tweets => {negative}')
        print(f'polarity => {polarity}')

query = input('What topic would you like to analyise: ')
print('Loading ...')
text_blob_sen = TextBlobSen(query)
text_blob_sen.analyise()
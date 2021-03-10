from textblob import TextBlob 
from dotenv import load_dotenv
import tweepy 
import os
from pathlib import Path

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

C_KEY = os.getenv('C_KEY')
C_SECRET = os.getenv('C_SECRET')
A_TOKEN = os.getenv('A_TOKEN')
A_SECRET = os.getenv('A_SECRET')

auth_handler = tweepy.OAuthHandler(consumer_key=C_KEY, consumer_secret=C_SECRET)
auth_handler.set_access_token(A_TOKEN, A_SECRET)

api = tweepy.API(auth_handler)

polarity = 0
positive = 0
negative = 0
neutral = 0

query = 'star wars'
tweet_num = 200

tweets = tweepy.Cursor(api.search, q=query, lang='en').items(tweet_num)

for tweet in tweets:
    trimmed_tweet = tweet.text.replace('RT', '')

    if trimmed_tweet.startswith(' @'): 
        index = trimmed_tweet.index(':')
        trimmed_tweet = trimmed_tweet[index + 2:]
    
    if trimmed_tweet.startswith('@'): 
        index = trimmed_tweet.index(' ')
        trimmed_tweet = trimmed_tweet[index + 2:]
    
    sentiment = TextBlob(trimmed_tweet)

    if sentiment.polarity > 0: positive += 1
    elif sentiment.polarity < 0: negative += 1
    elif sentiment.polarity == 0: neutral += 1

    polarity += sentiment.polarity

print(f'Analysis for {query}')

print(f'positive tweets => {positive}')
print(f'neutral tweets => {neutral}')
print(f'negative tweets => {negative}')
print(f'polarity => {polarity}')
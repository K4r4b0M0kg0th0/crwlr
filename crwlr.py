import tweepy
from textblob import TextBlob
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import argparse

nltk.download('stopwords')

# Authenticate to Twitter
consumer_key= 'Your_consumer_key'
consumer_secret= 'Your_consumer_secret'
access_token= 'Your_access_token'
access_token_secret= 'Your_access_token_secret'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Create API object
api = tweepy.API(auth)

# Create the parser
parser = argparse.ArgumentParser(description='Sentiment analysis tool that uses tweets about a specific topic to determine the overall sentiment of people discussing that topic.')

# Add the arguments
parser.add_argument('topic', type=str, help='The topic to search for')
parser.add_argument('--num_tweets', type=int, default=100, help='The number of tweets to analyze')
parser.add_argument('--lang', type=str, default='en', help='The language of the tweets')

# Parse the arguments
args = parser.parse_args()

topic = args.topic
num_tweets = args.num_tweets
lang = args.lang

def get_topic():
    topic = input("Enter the topic you want to search for: ")
    if not topic:
        print("Please enter a valid topic.")
        return get_topic()
    return topic

topic = get_topic()

# Initialize the sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# Initialize a variable to store the sentiment score
sentiment_score = 0

# Initialize the lemmatizer
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))

# Use Cursor to search for tweets
for tweet in tweepy.Cursor(api.search_tweets, q=topic, lang=lang).items(num_tweets):
    # Pre-processing
    tweet = re.sub(r'@\w+|https?:\/\/\S+', '', tweet.text) #remove punctuation
    tweet = tweet.lower() # lower case
    words = word_tokenize(tweet) # tokenize
    words = [word for word in words if word not in stop_words] # remove stop words
    words = [lemmatizer.lemmatize(word) for word in words] # lemmatize
    tweet = " ".join(words)
    sentiment_score += analyzer.polarity_scores(tweet)['compound']

# Calculate the average sentiment score
average_sentiment = sentiment_score / 100

# Print the average sentiment score
print("The overall sentiment of people discussing " + topic + " is " + str(average_sentiment))
import tweepy
from textblob import TextBlob
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

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

# Search for tweets about a specific topic
topic = "example"

# Initialize the sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# Initialize a variable to store the sentiment score
sentiment_score = 0

# Initialize the lemmatizer
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))

# Use Cursor to search for tweets
for tweet in tweepy.Cursor(api.search_tweets, q=topic).items(100):
    # Pre-processing
    tweet = re.sub(r'[^\w\s]','',tweet.text) #remove punctuation
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
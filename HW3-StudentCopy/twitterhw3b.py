# In this assignment you must do a Twitter search on any term
# of your choice.
# Deliverables:
# 1) Print each tweet
# 2) Print the average subjectivity of the results
# 3) Print the average polarity of the results

# Be prepared to change the search term during demo.
import tweepy
from textblob import TextBlob
import twittertoken

# Unique code from Twitter
access_token = twittertoken.access_token
access_token_secret = twittertoken.access_token_secret
consumer_key = twittertoken.consumer_key
consumer_secret = twittertoken.consumer_secret

# Boilerplate code here
auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)

api = tweepy.API(auth)
#Now we can Create Tweets, Delete Tweets, and Find Twitter Users

public_tweets = api.search('Golden State Warriors')


total_subjectivity = 0.0
total_polarity = 0.0
tweet_count = 0

for tweet in public_tweets:
	print(tweet.text)
	analysis = TextBlob(tweet.text)
	# print(analysis.sentiment)
	# print(analysis.sentiment.polarity)
	total_subjectivity += analysis.sentiment.subjectivity
	total_polarity += analysis.sentiment.polarity
	tweet_count += 1

#polarity -- measures how positive or negative
#subjectivity -- measures how factual.

#1 Sentiment Analysis - Understand and Extracting Feelings from Data

avg_subjectivity = total_subjectivity / tweet_count
avg_polarity = total_polarity / tweet_count

print()
print("Average subjectivity is", avg_subjectivity)
print("Average polarity is", avg_polarity)

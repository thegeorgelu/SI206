import tweepy
import nltk

# Unique code from Twitter
access_token = "232431314-h0uMw0glf8huuGREFviPQGVvUO8dEe1cObsVhUaO"
access_token_secret = "yPtYHFyEN3r3xkGSfJvRmbjor2gXbmbgKIjwdPhQqvctp"
consumer_key = "KdX3Wf20wCRdU6QYqbPz8vXO3"
consumer_secret = "wJkKUTfriRMJjWK8kf3pBDErDL6cxZCuamWLIwSPlP9jbpmV3F"

# Boilerplate code here
auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)

api = tweepy.API(auth)
#Now we can Create Tweets, Delete Tweets, and Find Twitter Users

public_tweets = api.search('UMSI')


adj_count = 0;

for tweet in public_tweets:
	print(tweet.text)
	tagged_tokens = nltk.pos_tag(tweet.text) # gives us a tagged list of tuples
	for (word, tag) in tagged_tokens:
		if tag == "JJ":
			adj_count+=1

print("There were ", adj_count,"adjectives in your tweets")
	
#Learn more about Search
#https://dev.twitter.com/rest/public/search


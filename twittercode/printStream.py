import tweepy
import json

# Unique code from Twitter
access_token = "232431314-h0uMw0glf8huuGREFviPQGVvUO8dEe1cObsVhUaO"
access_token_secret = "yPtYHFyEN3r3xkGSfJvRmbjor2gXbmbgKIjwdPhQqvctp"
consumer_key = "KdX3Wf20wCRdU6QYqbPz8vXO3"
consumer_secret = "wJkKUTfriRMJjWK8kf3pBDErDL6cxZCuamWLIwSPlP9jbpmV3F"

# Boilerplate code here
auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)

api = tweepy.API(auth)
def process_or_store(tweet):
	print(tweet.get('user').get('screen_name'))
	print(tweet.get('text').encode('unicode_escape'))
	print(tweet.get('created_at'))

for status in tweepy.Cursor(api.home_timeline).items(10):
    # Process a single status
    process_or_store(status._json) 


for tweet in tweepy.Cursor(api.user_timeline).items():
    process_or_store(tweet._json)



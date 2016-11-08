# Write a Python file that uploads an image to your 
# Twitter account.  Make sure to use the 
# hashtags #UMSI-206 #Proj3 in the tweet.

# You will demo this live for grading.

# print("""No output necessary although you 
# 	can print out a success/failure message if you want to.""")

import tweepy
from textblob import TextBlob
import os
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

img = os.path.abspath('kevin.jpg')
try:
	api.update_with_media(img, status="Hi David #UMSI-206 #Proj3")
	print("Success!")
except:
	print("Failed! :(")
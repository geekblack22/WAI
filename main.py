from random import sample
import database
import datetime
import algos
import sys
import twitterInterface
from dotenv import load_dotenv
import os 


def main():
	load_dotenv()
	
	consumer_key = os.getenv('consumer_key')
	consumer_secret = os.getenv('consumer_secret')
	server_1 = os.getenv('server_1')
	uid_1 = os.getenv('uid_1')
	database_1 = os.getenv('database_1')
	pwd_1 = os.getenv('pwd_1')
	server_2 = os.getenv('server_2')
	database_2 = os.getenv('database_2')
	uid_2 = os.getenv('uid_2')
	pwd_2 = os.getenv('pwd_2')

	print(pwd_1)


	# db = database.Database(server_1,database_1,uid_1,pwd_1)
	# tweets = db.getAllTweetsBetween(datetime.datetime(2020,11,1,0,0,0),datetime.datetime(2020,11,2,0,0,0))
	# median_tweets = algos.middle_n_entries(tweets, 10, database.retweet_compare, .85, .1)
	# new_db = database.Database(server_2,database_2,uid_2,pwd_2)
	# with open("tweetSample.txt",'w') as f:
	# 	[print(tweet.IDstr, file=f) for tweet in median_tweets]
	# with open("tweetSample.txt",'r') as f:
	# 		hamilton_tweets =  f.readlines()
	
	# for i in range(0,len(hamilton_tweets)):

	# 	hamilton_tweets[i] = hamilton_tweets[i].split(" ", 1)[0]

	# sample = twitterInterface.TwitterInterface(consumer_key,consumer_secret)
	# retweeters = []
	# # for tweet in median_tweets:
	# # 	retweeters.extend(sample.getRetweeters(tweet.IDstr))
	
	# # user_data = sample.getUsersData(retweeters) 
	# # print(user_data)
	# user1 = database.User("198765434","Human007",[],"2018-12-19 09:26:03.478039")
	# test_tweet = database.Tweet(5,"196765934","Human007")
	# # user_tweets = user1.tweets
	# # print(user_tweets[1].list_of_hashtags)
	# # print(user_tweets[1].IDstr)
	# # print(user_tweets[1].screenName)
	# # print(user_tweets[1].time)
	# new_db.insertUser(user1)
	# new_db.insertTweet(test_tweet)
	
	# # tweets = user1.tweets
	
	# # print(tweets[1].time)
	# # print(tweets[1].screenName)
	# #with open("tweetSample_pr.txt",'r') as f:
	# 	#hamilton_tweets = f.readlines()
	# #for i in range(0,20):
	# 	#hamilton_tweets[i] = hamilton_tweets[i].split(" ", 1)[0]
	# #sample = SampleTwitter.SampleTwitter(consumer_key,consumer_secret,hamilton_tweets)
	# #print(sample.getUserData(open("retweeterIDs.txt",'r').readlines()))

if __name__ == "__main__":
	main()


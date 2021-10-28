from random import sample
import database
from datetime import datetime, timedelta
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

	db = database.Database(server_1,database_1,uid_1,pwd_1)
	date = datetime.now()
	seeds = {}
	for i in range(15):
		for user in db.highestPercentGrowth(20,date):
			seeds[user] = 1
		date = date - timedelta(days = 30)
	
	[print(key) for key,value in seeds.items()]

	

	#with open("tweetSample.txt",'w') as f:
		#[print(tweet.IDstr, file=f) for tweet in median_tweets]
	#with open("tweetSample.txt",'r') as f:
			#hamilton_tweets =  f.readlines()
	
	#for i in range(0,len(hamilton_tweets)):

		#hamilton_tweets[i] = hamilton_tweets[i].split(" ", 1)[0]

	#sample = twitterInterface.TwitterInterface(consumer_key,consumer_secret)
	#retweeters = []
	#for tweet in median_tweets:
		#retweeters.extend(sample.getRetweeters(tweet.IDstr))
	
	#user_data = sample.getUsersData(retweeters) 
	#print(user_data)
	#user1 = user_data[0]
	#user_tweets = user1.tweets
	#print(user_tweets[1].list_of_hashtags)
	#print(user_tweets[1].IDstr)
	#print(user_tweets[1].screenName)
	#print(user_tweets[1].time)

	
	# tweets = user1.tweets
	
	# print(tweets[1].time)
	# print(tweets[1].screenName)
	#with open("tweetSample_pr.txt",'r') as f:
		#hamilton_tweets = f.readlines()
	#for i in range(0,20):
		#hamilton_tweets[i] = hamilton_tweets[i].split(" ", 1)[0]
	#sample = SampleTwitter.SampleTwitter(consumer_key,consumer_secret,hamilton_tweets)
	#print(sample.getUserData(open("retweeterIDs.txt",'r').readlines()))

if __name__ == "__main__":
	main()

from random import sample
import database
from datetime import datetime, timedelta
import algos
import sys
import twitterInterface
from dotenv import load_dotenv
import os 
import time
import pickle

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
	bearer_token = os.getenv('test_token')
	

	db = database.Database(server_1,database_1,uid_1,pwd_1)
	db2 = database.Database(server_2,database_2,uid_2,pwd_2)
	date = datetime.now()
	seeds = {}
	for i in range(15):
		for user in db.highestPercentGrowth(20,date):
			seeds[user] = 1
		date = date - timedelta(days = 30)
	
	sample = twitterInterface.TwitterInterface(consumer_key,consumer_secret,bearer_token)
	

	print(len(seeds))
	superTable = {}
	n = 0
	for key,value in seeds.items():
		engaged_users, freqs = sample.mostEngagedUsers(key,300,.05,n)
		for key_i,value_i in zip(engaged_users,freqs):
			if key_i in superTable:
				(superTable[key_i]).append((value_i,key))
			else:
				superTable[key_i] = [(value_i, key)]
			print(superTable[key_i])
		n += 1
	

	# table = open('table.pickle', 'wb')
	# pickle.dump(superTable,table)
	#tweets = sample.scrapeAllTweets('2318647908',all_tweets=False,num_tweets=1000)
	user = sample.scrapeUserData('2318647908')
	tweets = user.tweets
	print(user.creationDate)
	print(user.follower_count)
	print(user.tweet_count)
	for tweet in tweets:
	 	print(tweet)

	table = open('table.pickle', 'wb')
	pickle.dump(superTable,table)

if __name__ == "__main__":
	main()


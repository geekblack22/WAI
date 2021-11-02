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
	date = datetime.now()
	seeds = {}
	for i in range(15):
		for user in db.highestPercentGrowth(20,date):
			seeds[user] = 1
		date = date - timedelta(days = 30)
	
	sample = twitterInterface.TwitterInterface(consumer_key,consumer_secret,bearer_token)
	

	superTable = {}
	n = 0
	for key,value in seeds.items():
		print(n)
		n += 1
		engaged_users, freqs = sample.mostEngagedUsers(key,300,.05)
		for key_i,value_i in zip(engaged_users,freqs):
			superTable[key_i] = (value_i, key)
	
	table = open('table.pickle', 'wb')
	pickle.dump(superTable,table)
	# tweets = sample.scrapeAllTweets('2318647908')
	# for tweet in tweets:
		
	# 	print(
	# 	 "TweetID: "+ str(tweet.IDstr)
	# 	+" posterID: "+ str(tweet.posterID)
	# 	+" retweets: "+str(tweet.retweets)
	# 	+" time: " + str(tweet.time)
	# 	+" contains_video: " + str(tweet.contains_video)
	# 	+" list_of_hashtags: " + str(tweet.list_of_hashtags)
	# 	+" num_photos: "  + str(tweet.num_photos)
	# 	+" mentioned_ids: " + str(tweet.mentioned_ids)
	# 	)

if __name__ == "__main__":
	main()


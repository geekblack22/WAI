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
	

	#db = database.Database(server_1,database_1,uid_1,pwd_1)
	db2 = database.Database(server_2,database_2,uid_2,pwd_2)
	tw = twitterInterface.TwitterInterface(consumer_key,consumer_secret,bearer_token)

	# users = db.getAllEUsers()
	# [print(user[0], user[1], user[2], user[3], user[4], user[5]) for user in users]
	start = datetime(2020,11,17).strftime("%Y-%m-%d")
	end = datetime(2021,11,17).strftime("%Y-%m-%d")
	# #tweets  = tw.getTweetsBetween("barackobama",start,end)
	# users = db2.getAllUsers()
	# my_file = open("skip_user.txt", "r")
	# content = my_file.read()
	# skip_list = content.split("\n")
	# skip_list = [user.strip() for user in skip_list]
	ids = ["1272770461357584384","1583490801696633544","1276897886668800000","1219155179561521152","1036778724","992724216809127936","1287724171145994240"]
	
	hash,freq,dates= db2.hashtagProportions(ids,start,end)
	
	print(hash)
	print(freq)
	print(len(dates[1]))
	print(len(dates[0]))
	# my_file.close()
	# print(skip_list)
	# for user in skip_list:
	# 	name = tw.scrapeUsername(user)
	# 	tweets = tw.getTweetsBetween(name,start,end)
	# 	for tweet in tweets:
	# 		db2.updateUserTweets(tweet)
	# 	db2.cursor.commit()
	# 	print(str(skip_list.index(user)+1)+" users of "+ str(len(skip_list)))
	# for user in users:
	# 	tweets = []
	# 	print(user.IDstr.strip())
	# 	if user.IDstr.strip() in skip_list or (user.IDstr.strip() == "1407189773651898368" or user.IDstr.strip() == "1381149615467159552" or user.IDstr.strip() == "113410319"):
	# 		print("User tweets already inserted")
	# 		continue
	# 	else:
	# 		try:
			
	# 			name = tw.scrapeUsername(user.IDstr.strip())
	# 			if str(name)!= '\\NA\\':
	# 				tweets = tw.getTweetsBetween(name,start,end)
	# 		except:
	# 			tweets = []
	# 			print("deleted user")
	# 		if tweets != []:
	# 			for tweet in tweets:
	# 				print(str(users.index(user)+1)+" users of "+ str(len(users)))
	# 				db2.insertTweet(tweet)
	# 			db2.cursor.commit()
	# 			print("commit")
	# 			my_file = open("./skip_user.txt", "a")
	# 			my_file.write(str(user.IDstr.strip())+"\n")
	# my_file.close()	

	# 	# for tweet in tweets:
	# 	# 	db2.insertTweet(tweet)
	#my_file.close()

	
			
'''
	for user in users:
		if db.hasInfo(user.ID):
			continue
		try:
			uname = tw.scrapeUsername(str(user.IDstr).strip())
		except KeyError:
			print(uname)
			db.addInfo(user.ID, None, None, None, None, None)
			db.cursor.commit()
		percent = sum([1 for c in uname if c.isupper()])/len(uname)

		countries = user.getCountries(db2)
		print(uname)
		db.addInfo(user.ID, user.matches(uname), percent, countries['ir'], countries['ch'], countries['ru'])
		db.cursor.commit()

'''

if __name__ == "__main__":
	main()


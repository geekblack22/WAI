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
	

	db = database.Database(server_2,database_2,uid_2,pwd_2)
	db2 = database.Database(server_1,database_1,uid_1,pwd_1)
	tw = twitterInterface.TwitterInterface(consumer_key,consumer_secret,bearer_token)

	users = db.getAllEUsers()
	[print(user[0], user[1], user[2], user[3], user[4], user[5]) for user in users]

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


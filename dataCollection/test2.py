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
import visualizer


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
tw = twitterInterface.TwitterInterface(consumer_key,consumer_secret,bearer_token)

def getCountry(user):
	countries = user.getCountries(db)
	c = max(zip(countries.values(), countries.keys()))[1]
	return c

users = db2.getAllUsers()

table = db2.userTweetTable()

for userID, lot in table:
	print(userID, len(lot))

#users = filter(lambda u : getCountry(u) == 'ru', users)

#visualizer.plot_som_series_averaged_center(*algos.getClusters(users))

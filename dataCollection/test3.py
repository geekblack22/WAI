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

users = None
with open('userTweetTable.pickle', 'rb') as handle:
    users = pickle.load(handle)
updU = []
i=0
for user,l in users:
	user = db2.getUsertp(user)
	user.fingerprint = (user.mod([datetime.strptime("{0} {1} {2} {3}".format(*date.split()), "%b %d %Y %I:%M%p").time() for date in l.split(",")]))
	updU.append(user)
	print(i, "users done")
	i+=1
	print(user.fingerprint)

ch = filter(lambda u : getCountry(u) == 'ch', updU)

visualizer.plot_som_series_averaged_center(*algos.getClusters(ch))
ir = filter(lambda u : getCountry(u) == 'ir', updU)

visualizer.plot_som_series_averaged_center(*algos.getClusters(ir))
ru = filter(lambda u : getCountry(u) == 'ru', updU)

visualizer.plot_som_series_averaged_center(*algos.getClusters(ru))

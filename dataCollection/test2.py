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


#users = db2.getAllUsers()

#ch = filter(lambda u : getCountry(u) == 'ch', users)
#ir = filter(lambda u : getCountry(u) == 'ir', users)
#ru = filter(lambda u : getCountry(u) == 'ru', users)

users = None
with open('userTweetTable.pickle', 'rb') as handle:
    users = pickle.load(handle)

chU = filter(lambda u : getCountry(db2.getUsertp(u[0])) == 'ch', users)
irU = filter(lambda u : getCountry(db2.getUsertp(u[0])) == 'ir', users)
ruU = filter(lambda u : getCountry(db2.getUsertp(u[0])) == 'ru', users)

ch = []
ir = []
ru = []
i=0

for key,value in chU:
	print(i)
	i+=1
	ch.extend([datetime.strptime("{0} {1} {2} {3}".format(*date.split()), "%b %d %Y %I:%M%p") for date in value.split(",")])
for key,value in irU:
	print(i)
	i+=1
	ir.extend([datetime.strptime("{0} {1} {2} {3}".format(*date.split()), "%b %d %Y %I:%M%p") for date in value.split(",")])
for key,value in ruU:
	print(i)
	i+=1
	ru.extend([datetime.strptime("{0} {1} {2} {3}".format(*date.split()), "%b %d %Y %I:%M%p") for date in value.split(",")])

visualizer.plotWeek(ch)
visualizer.plotWeek(ir)
visualizer.plotWeek(ru)

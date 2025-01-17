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
# with open('userTweetTable.pickle', 'rb') as handle:
#     users = pickle.load(handle)
#users = db2.userTweetTable()
i = 0
#with open('userTweetTable.pickle', 'wb') as handle:
    #pickle.dump(users, handle, protocol=pickle.HIGHEST_PROTOCOL)
updU = db2.getAllUsers()
# for user,l in users:
# 	user = db2.getUsertp(user)
# 	user.fingerprint = (user.mod([datetime.strptime("{0} {1} {2} {3}".format(*date.split()), "%b %d %Y %I:%M%p").time() for date in l.split(",")]))
# 	updU.append(user)
# 	print(i, "users done")
# 	i+=1
# 	print(user.fingerprint)

ch = filter(lambda u : getCountry(u) == 'ir', updU)
ch_accounts = []
for i in ch:
	ch_accounts.append(i)
	

# # visualizer.plot_som_series_averaged_center(*algos.getClusters(ch))
# #ir = filter(lambda u : getCountry(u) == 'ir', updU)
#cluster = algos.getClusters(ch)
# updU = algos.getClusters(ch)[2][(0,1)]
# print(updU[0])
fingers = algos.getFingers(ch_accounts)
clusters = fingers.items()
clusters = [item for sublist in clusters for item in sublist]
clusters = [cluster for cluster in clusters if type(cluster) is not tuple]
clusters = [item for sublist in clusters for item in sublist]
print(clusters)
# Here d_items is a
visualizer.generateTimelines(clusters,"Iran")
#visualizer.plot_som_series_averaged_center(*algos.getClusters(ir))
# ru = filter(lambda u : getCountry(u) == 'ru', updU)

# visualizer.plot_som_series_averaged_center(*algos.getClusters(ru))

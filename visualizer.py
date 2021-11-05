import numpy as np
import matplotlib.pyplot as plt
import twitterInterface 
import os
import algos
import datetime
from dotenv import load_dotenv
retweeters = [2721413702,2897373563,1282456897,2541012107,1039900418686500865,1016733350785007616,388736352,239619301,803939316871393280,767270527,317302594,985220102483333120,2335406749,2609222612,2721957062]
n = np.arange(len(retweeters))
y = np.zeros_like(n) + 1
users = []
dates = []
load_dotenv()
consumer_key = os.getenv('consumer_key')
consumer_secret = os.getenv('consumer_secret')
bearer_token = os.getenv('test_token')

tw = twitterInterface.TwitterInterface(consumer_key,consumer_secret,bearer_token)

for retweeter in retweeters:
    try:
        users.append(tw.scrapeUserData(str(retweeter), get_tweets= False))
    except:
        print("User not found")

for user in users:
    date = user.creationDate
    dates.append(user.creationDate)
def compare(account1,account2):
    diff = account2.creationDate - account1.creationDate
    return diff.total_seconds()


clusters = algos.cluster(users,2,907200,compare,compare)
print(clusters)
list_2015 = [date for date in dates if date.year < 2015]
list_2016 = [date for date in dates if date.year == 2016]
list_2017 = [date for date in dates if date.year == 2017]
list_2018 = [date for date in dates if date.year == 2018]
list_2019 = [date for date in dates if date.year == 2019]
list_2020 = [date for date in dates if date.year == 2020]
list_2021 = [date for date in dates if date.year == 2021]
n = np.arange(len(retweeters))
y = np.zeros_like(n) + 1
print(len(users))


# fig, (year_1,year_2,year_3,year_4,year_5,year_6,year_7) = plt.subplots(7,figsize=(50, 50))
# fig.suptitle('Acount Creation Dates')
plt.figure(1)
plt.scatter(list_2015,np.zeros_like(list_2015) + 0, marker='o', c='red', lw=5)
plt.gcf().autofmt_xdate()
plt.figure(2)
plt.scatter(list_2016,np.zeros_like(list_2016) + 0, marker='o', c='red', lw=5)
plt.gcf().autofmt_xdate()
plt.figure(3)
plt.scatter(list_2017,np.zeros_like(list_2017) + 0, marker='o', c='red', lw=5)
plt.gcf().autofmt_xdate()
plt.figure(4)
plt.scatter(list_2018,np.zeros_like(list_2018) + 0, marker='o', c='red', lw=5)
plt.gcf().autofmt_xdate()
plt.figure(5)
plt.scatter(list_2019,np.zeros_like(list_2019) + 0, marker='o', c='red', lw=5)
plt.gcf().autofmt_xdate()
plt.figure(6)
plt.scatter(list_2020,np.zeros_like(list_2020) + 0, marker='o', c='red', lw=5)
plt.gcf().autofmt_xdate()
plt.figure(7)
plt.scatter(list_2021,np.zeros_like(list_2021) + 0, marker='o', c='red', lw=5)


plt.gcf().autofmt_xdate()
plt.show()
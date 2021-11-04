import numpy as np
import matplotlib.pyplot as plt
import twitterInterface 
import os
from dotenv import load_dotenv
retweeters = [995265275481284608,
1413480523461058562,
1285501984888557569,
1260509983638056963,
1404849002072317952,
1317199442777415681,
4492447474,
1404933060877979648,
2891463597,
1453004764212563991]
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
    users.append(tw.scrapeUserData(str(retweeter), get_tweets= False))
for user in users:
    dates.append(user.creationDate)
print(len(dates))
plt.scatter(dates,y, ls='dotted', c='red', lw=2)
plt.gcf().autofmt_xdate()
plt.show()
import numpy as np
import matplotlib.pyplot as plt
import twitterInterface 
import os
import algos
import datetime
import database
from dotenv import load_dotenv
from scipy.stats import chi2, loglaplace
from datetime import timedelta  
from labellines import labelLine, labelLines
from matplotlib import rcParams, cycler
import matplotlib.backends.backend_pdf
retweeters = [2721413702,2897373563,1282456897,2541012107,1039900418686500865,1016733350785007616,388736352,239619301,803939316871393280,767270527,317302594,985220102483333120,2335406749,2609222612,2721957062]
n = np.arange(len(retweeters))
y = np.zeros_like(n) + 1
users = []
dates = []
load_dotenv()
consumer_key = os.getenv('consumer_key')
consumer_secret = os.getenv('consumer_secret')
bearer_token = os.getenv('test_token')
server_1 = os.getenv('server_1')
uid_1 = os.getenv('uid_1')
database_1 = os.getenv('database_1')
pwd_1 = os.getenv('pwd_1')
server_2 = os.getenv('server_2')
database_2 = os.getenv('database_2')
uid_2 = os.getenv('uid_2')
pwd_2 = os.getenv('pwd_2')
db = database.Database(server_1,database_1,uid_1,pwd_1)
db2 = database.Database(server_2,database_2,uid_2,pwd_2)

users = db2.getAllUsers()
tw = twitterInterface.TwitterInterface(consumer_key,consumer_secret,bearer_token)

# for retweeter in retweeters:
#     try:
#         users.append(tw.scrapeUserData(str(retweeter), get_tweets= False))
#     except:
#         print("User not found")


def compare(account1,account2):
    diff = account2.creationDate - account1.creationDate
    return diff.total_seconds()
def dist(account1,account2):
    return abs(compare(account1,account2))

clusters = algos.cluster(users,15,1209600,compare,dist)
cluster_dates = [[user.creationDate for user in cluster] for cluster in clusters]

custer_engagement =  [[user.engagement for user in cluster] for cluster in clusters]



def engagementMap(users):
    engagement_dict = {}
    for user in users:
        for engagemet in user.engagement:
            if engagemet[1] in engagement_dict:
                engagement_dict[engagemet[1]].append(user.creationDate)
            else:
                engagement_dict[engagemet[1]] = [user.creationDate]
    return engagement_dict

cluster_maps = [engagementMap(cluster) for cluster in clusters]
cluster_users = [item for sublist in clusters for item in sublist]
full_map = engagementMap(cluster_users)

def plotEngagemetMap(engagement_dict,y,all_dates,large_data = False):
    mid_ys = []
    mid_dates = []
    
    NUM_COLORS = len(engagement_dict)
    cm = plt.get_cmap('jet')
    rcParams['axes.prop_cycle'] = cycler(color=cm(np.linspace(0, 1, NUM_COLORS)))
    scale = 100
    if large_data:
        scale = 2
    
    for key,engagers in engagement_dict.items():
        
        plt.rcParams["figure.autolayout"] = True
        dates = [date.strftime('%m/%d/%Y') for date in all_dates]
        res = [dates.index(i.strftime('%m/%d/%Y')) for i in engagers]
        y_line = [y[ind] for ind in res]
        seed_user = db.getUsername(str(key))
        overlapping = .75
        max_date = max(engagers)
        min_date = min(engagers)
        mid_date = min_date + (max_date - min_date)/2
        max_y = y_line[engagers.index(max_date)]
        min_y = y_line[engagers.index(min_date)]
        mid_y = min_y + (max_y - min_y)/2
        distance = (max_date - min_date)
        size = max_y - min_y
        print(size)
        # plt.plot(engagers,y_line, alpha = overlapping)
        
        # lines = plt.gca().get_lines()
        # l1=lines[-1]
        # x_data = l1.get_xdata()
        # y_data = l1.get_ydata()
        # y_label = y_data[-1]
        # x_label = x_data[-1]
        
        plt.plot(engagers,y_line,color = "green")
        plt.scatter(engagers,y_line,s = scale * len(engagers), alpha = overlapping,label = seed_user)
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))      
        ax.axes.yaxis.set_visible(False)


# print(custer_engagement)
all_dates = []

for i in range (0,len(cluster_dates)):
    x_poses = []
    y_poses = []
    texts = []
    fig = plt.figure()
    ax = plt.gca()
    fig.suptitle("Cluster "+str(i)+" Engagement Map", fontsize=20)
    all_dates.extend(cluster_dates[i])
    y = np.random.uniform(low = 0,high = 200,size=len(cluster_dates[i]))
    plotEngagemetMap(cluster_maps[i],y,cluster_dates[i])
    ax.set_yscale('log')
    plt.scatter(cluster_dates[i],y, marker='o', c='black', lw=.5)
    
    plt.gcf().autofmt_xdate()
    ax.axes.yaxis.set_visible(False)
    fig.savefig("Cluster"+str(i)+"_Engagement Map.jpeg")
    for i in range(len(texts)):
        plt.annotate(texts[i],(x_poses[i],y_poses[i]), rotation = 90, textcoords="offset points", 
                xytext=(0,10),
                ha='center')
        print(texts[i] + " X: "+ str(x_poses[i]) + " Y: "+ str(y_poses[i]))
fig = plt.figure()
ax = plt.gca()
fig.suptitle("Inter-Cluster Engagement Map", fontsize=20)
y = np.random.normal(size=len(all_dates))

x_poses = []
y_poses = []
texts = []

ax.axes.yaxis.set_visible(False)
plt.scatter(all_dates,y, marker='o', c='black', lw=.5)
plotEngagemetMap(full_map,y,all_dates,large_data= True)

# for i in range(len(texts)):
#     plt.annotate(texts[i],(x_poses[i],y_poses[i]), rotation = 90, textcoords="offset points", 
#             xytext=(0,6),
#             ha='center')
#     print(texts[i] + " X: "+ str(x_poses[i]) + " Y: "+ str(y_poses[i]))


plt.gcf().autofmt_xdate()
fig.savefig("Inter-Cluster_Engagement_Map.jpeg")
plt.show()





# # fig, (year_1,year_2,year_3,year_4,year_5,year_6,year_7) = plt.subplots(7,figsize=(50, 50))
# # fig.suptitle('Acount Creation Dates')
# plt.figure(1)
# plt.scatter(list_2015,np.zeros_like(list_2015) + 0, marker='o', c='red', lw=5)
# plt.gcf().autofmt_xdate()
# plt.figure(2)
# plt.scatter(list_2016,np.zeros_like(list_2016) + 0, marker='o', c='red', lw=5)
# plt.gcf().autofmt_xdate()
# plt.figure(3)
# plt.scatter(list_2017,np.zeros_like(list_2017) + 0, marker='o', c='red', lw=5)
# plt.gcf().autofmt_xdate()
# plt.figure(4)
# plt.scatter(list_2018,np.zeros_like(list_2018) + 0, marker='o', c='red', lw=5)
# plt.gcf().autofmt_xdate()
# plt.figure(5)
# plt.scatter(list_2019,np.zeros_like(list_2019) + 0, marker='o', c='red', lw=5)
# plt.gcf().autofmt_xdate()
# plt.figure(6)
# plt.scatter(list_2020,np.zeros_like(list_2020) + 0, marker='o', c='red', lw=5)
# plt.gcf().autofmt_xdate()
# plt.figure(7)
# plt.scatter(list_2021,np.zeros_like(list_2021) + 0, marker='o', c='red', lw=5)



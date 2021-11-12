import numpy as np
import matplotlib.pyplot as plt
from numpy.core.defchararray import startswith
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
all_user_dates = [user.creationDate for user in users]
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
full_user_map = engagementMap(users)


def plotSegmentedEngagementMap(engagement_dict,y,cluster_users,all_dates,x_label,y_label,large_data = False):
    i = 0
    for key,engagers in engagement_dict.items():
        i+=1
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
        engagement = [[engagement[0] for engagement in user.engagement] for user in cluster_users]
        engagement =  [item for sublist in engagement for item in sublist]
        size = [engagement[ind] for ind in res]
       
        max_size = max(size)
     
        print(max_size)
        print("size: " + str(size))
        size = [min(s*20,50) if s < 22 else s for s in size]
        fig = plt.figure()  
        fig.suptitle(str(seed_user)+" Engagement Map", fontsize=20) 
        ax = plt.gca()
        ax.set_xlabel(x_label, fontsize=10)
        ax.set_ylabel(y_label, fontsize=10)
        # plt.scatter(engagers,y_line,color = "black")
        plt.scatter(engagers,y_line,s = size,color = "red", alpha = overlapping)
        plt.gcf().autofmt_xdate()

def plotFingerPrint(user):
	fingerPrint = user.getFingerprint()
    # plt.figure()
	count, bins_count = np.histogram(fingerPrint, bins=25)
	pdf = count / sum(count)
	cdf = np.cumsum(pdf)
	print(len(fingerPrint))
	x = np.arange(0,25)
	plt.plot(x,fingerPrint)

# def getNumFollowers(user):
#     return user.follower_count
# def getNum(user):
#     return user.tweet_count
# def getSeedUsers(user):
#     return [engagement[1] for engagement in user.engagement] 
# def common_member(a, b):
#     a_set = set(a)
#     b_set = set(b)
 
#     if (a_set & b_set):
#         return (a_set & b_set)
# def returnCrossEngagement(cluster_1,Cluster_2):
#    for user in cluster_1:
#        for usr in Cluster_2:
           

# def intraClusterMap(clusters,count):
#     x = []
#     y = []

#     for cluster in clusters:
#         for user in cluster:
#             for
def plotEngagemetMap(engagement_dict,y,cluster_users,all_dates,x_label,y_label,large_data = False,segment = False):
    mid_ys = []
    mid_dates = []
    
    NUM_COLORS = len(engagement_dict)
    cm = plt.get_cmap('jet')
    rcParams['axes.prop_cycle'] = cycler(color=cm(np.linspace(0, 1, NUM_COLORS)))
    scale = 400
    if large_data:
        scale = 60
    
    
    i = 0
    fig = plt.figure()
    ax = plt.gca()
    ax.set_xlabel(x_label, fontsize=10)
    ax.set_ylabel(y_label, fontsize=10)
    plt.scatter(all_dates,y, marker='o', c='black', lw=.25)
    for key,engagers in engagement_dict.items():
        i+=1
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
        engagement = [[engagement[0] for engagement in user.engagement] for user in cluster_users]
        engagement =  [item for sublist in engagement for item in sublist]
        size = [engagement[ind] for ind in res]
       
        max_size = max(size)
     
        print(max_size)
        print("size: " + str(size))
        size = [min(s*20,50) if s < 22 else s for s in size]
        print("resize: " + str(size))
      

        
        # plt.plot(engagers,y_line, alpha = overlapping)
    
        # lines = plt.gca().get_lines()
        # l1=lines[-1]
        # x_data = l1.get_xdata()
        # y_data = l1.get_ydata()
        # y_label = y_data[-1]
        # x_label = x_data[-1]
        
        plt.scatter(engagers,y_line,s = size, alpha = overlapping)
        plt.plot(engagers,y_line,label = seed_user)
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))   
        plt.gcf().autofmt_xdate()   
        # ax.axes.yaxis.set_visible(False)


# print(custer_engagement)
all_dates = []

# for i in range (0,len(cluster_dates)):
#     x_poses = []
#     y_poses = []
#     texts = []
#     fig = plt.figure()
#     ax = plt.gca()
#     fig.suptitle("Cluster "+str(i)+" Engagement Map", fontsize=20)
#     all_dates.extend(cluster_dates[i])
#     y = [user.tweet_count for user in clusters[i]]
#     plotEngagemetMap(cluster_maps[i],y,clusters[i],cluster_dates[i])
#     # ax.set_yscale('log')
#     ax.set_xlabel("Creation Dates", fontsize=10)
#     ax.set_ylabel("Tweet Count", fontsize=10)
#     plt.scatter(cluster_dates[i],y, marker='o', c='black', lw=.25)
    
#     plt.gcf().autofmt_xdate()
#     # ax.axes.yaxis.set_visible(False)
#     fig.savefig("Cluster"+str(i)+"_Engagement Map.jpeg")
   
# fig = plt.figure()
# ax = plt.gca()
# fig.suptitle("Inter-Cluster Engagement Map", fontsize=20)
# ax.set_xlabel("Creation Dates", fontsize=10)
# ax.set_ylabel("Tweet Count", fontsize=10)

y = [user.tweet_count for user in users]

x_poses = []
y_poses = []
texts = []

# ax.axes.yaxis.set_visible(False)
# plt.scatter(all_dates,y, marker='o', c='black', lw=.25)
# plotEngagemetMap(full_map,y,cluster_users,all_dates,large_data= True)
#newus = []
#for user in users:
#	countries = user.getCountries(db)
#	if not (countries['ch'] > countries['ir'] and countries['ch'] > countries['ru']):
#		newus.append(user)	
#users = newus
		
fingerprintCluster = algos.fingerprintCluster(users, 30)
fingerprintCluster.append(users)

fig, ax = plt.subplots()
irs = np.array([])
chs = np.array([])
rus = np.array([])

irstd = np.array([])
chstd = np.array([])
rustd = np.array([])
for cluster in fingerprintCluster:
	ir = 0
	ch = 0
	ru = 0
	iri = np.array([])
	chi = np.array([])
	rui = np.array([])
	s = 0
	for user in cluster:
		countries = user.getCountries(db)
		iri = np.append(iri,countries['ir'])
		chi = np.append(chi,countries['ch'])
		rui = np.append(rui,countries['ru'])
	ir = sum(iri)
	ch = sum(chi)
	ru = sum(rui)
	s = ir+ru+ch
	irstd = np.append(irstd,np.std(iri/s))
	chstd = np.append(chstd,np.std(chi/s))
	rustd = np.append(rustd,np.std(rui/s))
	print(ir/s,ch/s,ru/s,ir/s+ch/s+ru/s, irstd[-1])
	irs = np.append(irs,ir/s)
	chs = np.append(chs,ch/s)
	rus = np.append(rus,ru/s)
	

width = .75
labels = [str(x) for x in range(30)] + ["all"]

ax.bar(labels, irs, width, yerr = irstd, label='ir')
ax.bar(labels, chs, width, yerr = chstd, bottom = irs, label='ch')
ax.bar(labels, rus, width, yerr = rustd, bottom = chs+irs,label='ru')
ax.legend()


		
		
		
		
    #fig.savefig("Cluster_"+str(fingerprintCluster.index(cluster))+"_Fingerprint.jpeg")
# vals = ax.get_yticks()
# ax.set_yticklabels(['{:,.2%}'.format(x) for x in vals])
# plotEngagemetMap(full_user_map,y,users,all_user_dates,segment=True)


# for i in range(len(texts)):
#     plt.annotate(texts[i],(x_poses[i],y_poses[i]), rotation = 90, textcoords="offset points", 
#             xytext=(0,6),
#             ha='center')
#     print(texts[i] + " X: "+ str(x_poses[i]) + " Y: "+ str(y_poses[i]))


# plt.gcf().autofmt_xdate()
# fig.savefig("Inter-Cluster_Engagement_Map.jpeg")
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



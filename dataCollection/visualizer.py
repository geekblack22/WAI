import numpy as np
import matplotlib.pyplot as plt
from numpy.core.defchararray import startswith
import twitterInterface 
import os
from statistics import mean
import algos
import datetime
import database
from dotenv import load_dotenv
from scipy.stats import chi2, loglaplace 
from datetime import datetime, timedelta
from labellines import labelLine, labelLines
from matplotlib import rcParams, cycler
import matplotlib.backends.backend_pdf
import matplotlib.dates as mdates
import random
import calendar
import matplotlib as mpl
import scipy.stats as stats

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

#clusters = algos.cluster(users,15,1209600,compare,dist)
#cluster_dates = [[user.creationDate for user in cluster] for cluster in clusters]
#all_user_dates = [user.creationDate for user in users]
#custer_engagement =  [[user.engagement for user in cluster] for cluster in clusters]
#fingers = algos.fingerprintCluster(users,30)

def plotTimes(user):
	fig = plt.figure(figsize=(20, 20))
	ax = plt.gca()
	tweets = db2.getAllTweetsByUserID(user.IDstr)
	tweets.sort(key=lambda e : e.time)
	diffs = [0] * (len(tweets)-1)
	i = 0
	for tweet1,tweet2 in zip(tweets[0:-2],tweets[1:-1]):
		diffs[i] = (tweet2.time - tweet1.time).total_seconds()/60
		i+=1
	print(diffs)
	plt.hist(diffs,bins=100)
	plt.show()

#for user in users:
	#plotTimes(user)

def engagementMap(users):
    engagement_dict = {}
    for user in users:
        for engagemet in user.engagement:
            if engagemet[1] in engagement_dict:
                engagement_dict[engagemet[1]].append(user)
            else:
                engagement_dict[engagemet[1]] = [user]
    return engagement_dict

#cluster_maps = [engagementMap(cluster) for cluster in clusters]
#cluster_users = [item for sublist in clusters for item in sublist]
#full_map = engagementMap(cluster_users)
#full_user_map = engagementMap(users)


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
	end_date = datetime(2021,11,8)
	dates = []
	date = end_date
	for i in range(25):	
		dates.append(date)
		date = date - timedelta(days=15)
	dates.reverse()   
	
	count, bins_count = np.histogram(fingerPrint, bins=25)
	pdf = count / sum(count)
	cdf = np.cumsum(pdf)
	print(len(fingerPrint))
	x = np.arange(0,25)

	plt.plot(dates,fingerPrint)
	plt.gcf().autofmt_xdate()  

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
# 
#            for
def pairEngagement(list):
	pairs = []
	print("list: ", list)
	for i in range(len(list)):
		for j in range(i+1, len(list)):
			tupple = (list[i],list[j])
			pairs.append(tupple)
			print(tupple)
	return pairs

def summary(som_x, som_y, win_map_toData, win_map_toAcc, axis, folderName):
	os.mkdir(folderName)
	#fig.suptitle('Clusters')
	for x in range(som_x):
		for y in range(som_y):
			fig, axs = plt.subplots(figsize=(25,25))
			cluster = (x,y)
			cluster_number = x*som_y+y+1
			os.mkdir(folderName + "/" + str(cluster_number))
			txt = open(f"{folderName}/{cluster_number}/accounts.txt", "w")
			if cluster in win_map_toData.keys():
				for series,account in zip(win_map_toData[cluster],win_map_toAcc[cluster]):
					print(account.IDstr)
					plt.plot(series,c="gray",alpha=0.5) 
					txt.write(account.IDstr + "\n")
				plt.plot(np.average(np.vstack(win_map_toData[cluster]),axis=0),c="red")
				#print(cluster_number,len(win_map[cluster]))

			axs.set_title(f"Cluster {cluster_number}")
			txt.close()
			fig.savefig(f"{folderName}/{cluster_number}/frequencyGraph.jpg")
			generateTimelines(win_map_toAcc[cluster],f"cluster_{cluster_number}",f"{folderName}/{cluster_number}/")
	#plt.show()

def plot_som_series_averaged_center(som_x, som_y, win_map):
	fig, axs = plt.subplots(som_x,som_y,figsize=(25,25))
	fig.suptitle('Clusters')
	for x in range(som_x):
		for y in range(som_y):
			cluster = (x,y)
			cluster_number = x*som_y+y+1
			if cluster in win_map.keys():
				for series in win_map[cluster]:
					axs[cluster].plot(series,c="gray",alpha=0.5) 
				axs[cluster].plot(np.average(np.vstack(win_map[cluster]),axis=0),c="red")
				print(cluster_number,len(win_map[cluster]))
			axs[cluster].set_title(f"Cluster {cluster_number}")

	plt.show()


def plotWeek(lot):
	vals = list(map(lambda t : (t - datetime.datetime.combine(t.date() - (datetime.timedelta(days = t.weekday())), datetime.datetime.min.time())).total_seconds(), lot))
	print(vals)
	density = stats.gaussian_kde(vals)
	n, x, _ = plt.hist(vals, bins=365, histtype=u'step', density=True)
	plt.plot(x, density(x))
	plt.show()

def plotAllTweets(lou):
	u = []
	for user in lou:
		u.append(user.fingerprint)
	for user in u:
		plt.plot(user,c="gray",alpha=0.5) 

	plt.plot(np.sum(np.vstack(u),axis=0),c="red")
	plt.show()


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
#all_dates = []

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

#y = [user.tweet_count for user in users]

#x_poses = []
#y_poses = []
#texts = []

# ax.axes.yaxis.set_visible(False)
# plt.scatter(all_dates,y, marker='o', c='black', lw=.25)
# plotEngagemetMap(full_map,y,cluster_users,all_dates,large_data= True)
#newus = []
#for user in users:
#	countries = user.getCountries(db)
#	if not (countries['ch'] > countries['ir'] and countries['ch'] > countries['ru']):
#		newus.append(user)	
#users = newus
		
#fingerprintCluster = algos.fingerprintCluster(users, 30)
#fingerprintCluster.append(users)

def plotCountryBarGraph(fingerprintCluster):
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
def generateTimelines(users,country, loc = "./"):
	start = datetime(2020,11,17)
	end = datetime(2021,11,17)
	date = end
	dates = []
	all_hashtags = []
	all_dates = []
	ids = [user.IDstr.strip() for user in users]
	all_freq = []
	fig, ax = plt.subplots(4,3,figsize=(20,20))
	fig.subplots_adjust(hspace = .46, wspace=1)
	fig.suptitle(country, fontsize=16)
	ax = ax.ravel()
	for i in range(12):	
		previous_date = date
		days_in_month = calendar.monthrange(date.year, date.month)[1]
		date = date - timedelta(days=days_in_month)
		hashtags,freq, hash_dates = db2.hashtagProportions(ids,date,previous_date)
		plt.rcdefaults()
		y_pos = np.arange(len(hashtags))
		hashtags = list(set(hashtags))
		y_pos = np.arange(len(hashtags))
		ax[i].barh(y_pos, freq, align='center')
		print(freq)
		print(freq)
		ax[i].set_yticks(y_pos)
		ax[i].set_yticklabels(hashtags)
		ax[i].invert_yaxis()  # labels read top-to-bottom
		ax[i].set_xlabel('Number of Tweets')
		ax[i].set_title(date.strftime("%m/%d/%Y") + "-"+ previous_date.strftime("%m/%d/%Y"))
	fig.savefig(loc + country)
def plotfcs(fingerprintCluster):
	
	for cluster in fingerprintCluster:
		fig = plt.figure(figsize=(20, 20))
		ax = plt.gca()
		for user in cluster:
			plotFingerPrint(user)
		vals = ax.get_yticks()
		ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
		ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))
		ax.set_yticklabels(['{:,.2%}'.format(x) for x in vals])
		fig.savefig("Cluster_"+str(fingerprintCluster.index(cluster))+"_Fingerprint.jpeg")

#plotfcs(fingers)
# for i in range(len(texts)):
#     plt.annotate(texts[i],(x_poses[i],y_poses[i]), rotation = 90, textcoords="offset points", 
#             xytext=(0,6),
#             ha='center')
#     print(texts[i] + " X: "+ str(x_poses[i]) + " Y: "+ str(y_poses[i]))


# plt.gcf().autofmt_xdate()
# fig.savefig("Inter-Cluster_Engagement_Map.jpeg")
# plt.show()



	



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


#plt.show()

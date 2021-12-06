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
def generateTimelines(users,country):
	start = datetime(2020,11,17)
	end = datetime(2021,11,17)
	date = end
	dates = []
	all_hashtags = []
	all_dates = []
	ids = [user.IDstr.strip() for user in users]
	# ids = ["1272770461357584384","1583490801696633544","1276897886668800000","1219155179561521152","1036778724","992724216809127936","1287724171145994240"]
	
	print(ids)
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
		# print(date)
		# print(previous_date)
		# print(hashtags)
		# print(freq)
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

		# for j in range(len(hashtags)):
		# 	all_hashtags.extend([hashtags[j] for p in range(freq[j])])
		# hash_dates = [item for sublist in hash_dates for item in sublist]
		# all_dates.extend(hash_dates)
		
			
		# dates = [dates[random.randint(int((len(dates)-1)/2),len(dates)-1)] for dates in hash_dates]
		# dates = []
		# for dates_list in hash_dates:
		# 	for date in dates_list:
		# 		if date not in dates:
		# 			if dates != []:
		# 				if date - dates[len(dates) -1] <= timedelta(days=3) or dates[len(dates) -1] - date <= timedelta(days=3):
		# 					dates.append(date+timedelta(days= 3))
		# 					break
		# 			else:
		# 				dates.append(date)
		# 				break
		# all_dates.extend(dates)
			# if date == start:
			# 	break
		
		levels = []

		# for i in range(len(all_dates)):
		# 	if i%2== 0:
		# 		levels.append(i*30)
		# 	else:
		# 		levels.append(i*-30)
		# levels = np.tile([-15, 15, -13, 13, -10, 10, -30, -4],
        #          int(np.ceil(len(all_dates)/6)))[:len(all_dates)]
		# levels = np.array(levels)
		
		
		# for i in range(len(all_dates)):
		# 	if i%2== 0:
		# 		freq[i] = i*10
		# 	else:
		# 		freq[i] = i*-10
	# 	levels = np.array(freq)
	# fig, ax = plt.subplots(figsize=(5,5))
	# cmap = plt.cm.gist_rainbow
	# norm = mpl.colors.Normalize(vmin=0, vmax=len(all_hashtags) - 1)
	# colors = [cmap(norm(i)) for i in range(len(all_hashtags))]
	# # for x,y,c,lb in zip(all_dates,all_freq,colors,all_hashtags):
	# print(len(all_freq))
		
	# print(len(all_dates))
	# bar = ax.bar(all_dates, all_freq,edgecolor = "black")

	# for idx,rect in enumerate(bar):
	# 	height = rect.get_height()
	# 	ax.text(rect.get_x() + rect.get_width()/2., 1.07*height,
	# 			all_hashtags[idx],
	# 			ha='center', va='bottom', rotation=90,fontsize = 6)
	# ax.set_xticklabels(all_hashtags)
	# handles, labels = ax.get_legend_handles_labels()
	# by_label = dict(zip(labels, handles))
	# ax.legend(by_label.values(), by_label.keys(),loc='center left', bbox_to_anchor=(1, 0.5))
	

	# Create figure and plot a stem plot with the date

		
		# ax = plt.gca()
		# ax.set(title="Matplotlib release dates")

		# ax.vlines(all_dates, 0, levels, color="tab:red")  # The vertical stems.
		# ax.plot(all_dates, np.zeros_like(all_dates), "-o",
		# 		color="k", markerfacecolor="w")  # Baseline and markers on it.

		# # annotate lines
		# for d, l, r in zip(all_dates, levels, all_hashtags):
		# 	ax.annotate(r, xy=(d, l),
		# 				xytext=(-3, np.sign(l)*3), textcoords="offset points",
		# 				horizontalalignment="right" if l > 0 else "left",
		# 				verticalalignment="bottom" if l > 0 else "top",fontsize = 10)

		# # format xaxis with 4 month intervals
		# ax.xaxis.set_major_locator(mdates.DayLocator(interval=30))
		# ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))
		
		# # remove y axis and spines
		# ax.yaxis.set_visible(False)
		# ax.spines[["left", "top", "right"]].set_visible(False)
		# plt.setp(ax.get_xticklabels(), rotation=30, ha="right")
		
	
	plt.show()
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

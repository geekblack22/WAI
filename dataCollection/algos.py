import functools
import random
from sklearn.cluster import KMeans
import numpy as np
import math

from sklearn.preprocessing import MinMaxScaler

from minisom import MiniSom
from tslearn.barycenters import dtw_barycenter_averaging
from tslearn.clustering import TimeSeriesKMeans
from sklearn.cluster import KMeans

from sklearn.decomposition import PCA
'''
loe: list of entries (listof E)
n: number of entries to return
compare: compare function ((E, E)->number) for sorting

returns a list of n entries that are closest to the median.
'''
def middle_n_entries(loe, n, compare, percent, delta):
	loe_s = sorted(loe, key=functools.cmp_to_key(compare))
	ret = []
	for i in range(n):
		adding = loe_s.pop(int(len(loe_s) * (percent + random.uniform(-delta, delta))))
		ret.append(adding)
	return ret

'''
loe: list of entries (listof E)
threshold_number: number of entrees within a close time period before being flagged
threshold_time: if theshold_number of entries are within this time period, flag accounts
compare: compare function ((E, E)->number) for sorting
distnace: distnace function ((E, E)->number)

returns a list of clusters
'''
def cluster(loe, threshold_number, threshold_time, compare, distance):
	loe_s = sorted(loe, key=functools.cmp_to_key(compare))
	index = 0
	ret = []
	while index < len(loe_s):
		temp_index = index
		count = 0
		while distance(loe_s[index], loe_s[temp_index]) < threshold_time:
			count += 1
			temp_index += 1
			if temp_index == len(loe_s):
				break
		if count >= threshold_number:
			ret.append(loe_s[index:temp_index])
			index = temp_index

		else:
			index += 1

	return ret

def fingerprintCluster(lou, clusters):
	X = np.array([np.array(user.getFingerprint()) for user in lou])
	kmeans = KMeans(n_clusters=clusters, random_state=0).fit(X)
	ret = [0]*clusters
	for i in range(clusters):
		ret[i] = [user for n,user in enumerate(lou) if kmeans.labels_[n] == i]
	return ret


def highest_retweets_each_user(lot):
	highestTweets = {}
	ret = []
	for tweet in tweets:
		if tweet.screenName in highestTweets:
			if highestTweets[tweet.screenName].retweets < tweet.retweets:
				highestTweets[tweet.screenName] = tweet
		else:
			highestTweets[tweet.screenName] = tweet
	for handle in highestTweets:
		ret.append(highestTweets[handle].IDstr)
	return ret

def fingerprint(user, threshhold):
	starts = []
	ends = []
	for i in range(1,len(user.tweets)):
		if ((user.tweets[i] - user.tweets[i-1]).total_seconds() > threshhold):
			starts.append(user.tweets[i-1])
			ends.append(user.tweets[i])
	return (starts,ends)

def getFingers(lou,n=1):
	som_x,som_y,win_map,ret = backEndClusters(lou,n)
	return ret

def getClusters(lou,n=1):
	som_x,som_y,win_map,ret = backEndClusters(lou,n)
	return som_x,som_y,win_map

def backEndClusters(lou,n=1):
	series = []
	for user in lou:
		finger = user.fingerprint
		s = sum(finger)
		if s == 0.0:
			continue
		lst = []
		for i,dp in enumerate(finger[::n]):
			apd = sum([f/s for f in finger[n*i:n*i+n:]])
			lst.append(apd)
		series.append(lst)
	som_x = som_y = math.ceil(math.sqrt(math.sqrt(len(series))))
	som = MiniSom(som_x, som_y,len(series[0]), sigma=1, learning_rate = 0.1)

	som.random_weights_init(series)
	som.train(series, 50000)
	ret = {}
	for seri,user in zip(series,lou):
		w = som.winner(seri)
		if w in ret:
			ret[w].append(user)
		else:
			ret[w] = [user]
	return som_x,som_y,som.win_map(series),ret

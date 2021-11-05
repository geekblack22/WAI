import functools
import random
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


import tweepy
import numpy as np
import sys
import time
import database
from timeit import default_timer as timer
from collections import Counter
import requests
import snscrape.modules.twitter as sntwitter

class TwitterInterface:

	"""This class interfaces with the Twitter API"""

	def __init__(self,consumer_key,consumer_secret,bearer_token):
		self.consumer_key = consumer_key
		self.consumer_secret = consumer_secret
		self._auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
		self.api = tweepy.API(self._auth, wait_on_rate_limit=True)
		self.lastQ = timer()
		self._bearer_token = bearer_token
		self.client = tweepy.Client(bearer_token=self._bearer_token)

	def getRetweeters(self, twitter_id):
		print(twitter_id)
		self.rateLim()
		return self.api.get_retweeter_ids(twitter_id)

	def getLikingUsers(self,tweet_id):
		
		url = "https://api.twitter.com/2/tweets/"+tweet_id+"/liking_users&expansions=pinned_tweet_id&user.fields=created_at&tweet.fields=created_at" 
		headers = {"Authorization" : "Bearer {}".format(self._bearer_token)}
		response = requests.get(url,headers= headers)
		return response

	def  getUsersData(self, account_ids):
		"""Gets all the information pertaining to the users in the list of user IDs
		Parameters
		----------
		account_ids: list of str
			list of account IDs	
		Returns
		-------
		list
			a list of user objects
		 """
		results = []
		for i in range(0, len(account_ids)):
			results.extend(self.retrieveUsers([account_ids[i]]))
		return results
	def scrapeAllTweets(self,user_id):
		tweets = []
		hashtags = ""
		user_info = enumerate(sntwitter.TwitterUserScraper(user_id, isUserId = True).get_items())
		for i,tweet in user_info:
			
			photo_count,contains_video = self.scrapeMedia(tweet)
			if tweet.hashtags is not None:
				hashtags = ",".join(tweet.hashtags)
			tweets.append(
			database.Tweet(str(tweet.id),
			retweets=tweet.retweetCount,
			time = tweet.date,contains_video = contains_video, 
			num_photos= photo_count,posterID= user_id,
			list_of_hashtags= hashtags,
			mentioned_ids = self.getMentionedIDs(tweet.mentionedUsers))
			)
		profile_info = enumerate(sntwitter.TwitterProfileScraper(user_id, isUserId = True).get_items())
		for i,tweet in profile_info:
			retweet = tweet.retweetedTweet
			if not (retweet is None):
				photo_count,contains_video = self.scrapeMedia(retweet)
				if not (retweet.hashtags  is None):
					hashtags = ",".join(tweet.hashtags)
				user = retweet.user
				tweets.append(
				database.Tweet(str(retweet.id),
				retweets=retweet.retweetCount,
				time = retweet.date,contains_video = contains_video, 
				num_photos= photo_count,
				list_of_hashtags= hashtags,
				mentioned_ids = self.getMentionedIDs(tweet.mentionedUsers),isRetweet=True)
				)
		return tweets
	def getMentionedIDs(self,mentions):
		ids = []
		if not (mentions is None):
			for user in mentions:
				ids.append(user.id)
		return ids

	def scrapeMedia(self,tweet):
		contains_video = False
		photo_count = 0
		if not (tweet.media is None):
				for medium in tweet.media:
					if isinstance(medium, sntwitter.Photo):
						photo_count+=1
					contains_video = (isinstance(medium, sntwitter.Video) or isinstance(medium, sntwitter.VideoVariant))

			
		return photo_count,contains_video
  

	def retrieveUsers(self,list):
		"""Gets all the information about a list of users 
		Parameters
		----------
		list: list of str
			list of account IDs	
		Returns
		-------
		list
			a list of user objects
		 """
		users = [None]*len(list)
		for i in range(0,len(list)):
			self.rateLim()
			response = self.api.get_user(user_id = list[i])
			tweets =  self.getAllTweets(list[i])
			users[i] = database.User(list[i],tweets,response.created_at)
		return users

	def getAllTweets(self,id):
		"""gets all the tweets of a user  
		Parameters
		----------
		id: str 
			User ID assigned by Twitter 	
		Returns
		-------
		list
			a list of twitter objects
		 """
		self.rateLim()
		tweets = tweepy.Cursor(self.api.user_timeline,include_rts=False,user_id = id).items(1500)
		user_tweets = []
		for tweet in tweets:
			photo_count, contains_video = self._numMedia(tweet)
			creation_date = tweet.created_at
			retweets = tweet.retweet_count
			
			hashtags = tweet.entities.get("hashtags")
			if not (hashtags  is None):
				hashtags = ",".join([item['text'] for item in hashtags])
			else:
				hashtags = " "
			mentions = tweet.entities.get("user_mentions")
			mentioned_ids = []
			for mention in mentions:
				mentioned_ids.append(mention.get('id_str'))
			

			tweet_id_str = tweet.id_str
			tweet_object = database.Tweet(tweet_id_str,retweets = retweets,list_of_hashtags= hashtags,time=creation_date,contains_video = contains_video,num_photos= photo_count,mentioned_ids = mentioned_ids)
			user_tweets.append(tweet_object)
		return user_tweets

	def rateLim(self):
		now = timer()
		if (.35 - (now - self.lastQ) > 0):
			time.sleep(.35 - (now - self.lastQ))
		self.lastQ = timer()

	def _numMedia(self,tweet):
		"""determines the media in a tweet 
		Parameters
		----------
		tweet: Status object
			The json of the the attributes of a tweet as an object 	
		
		Returns
		-------
		int
			the number of photos in the tweet
		boolean
			if there are any videos in the tweet
		 """
		photo_count = 0
		contains_video = False
		for media in tweet.entities.get("media",[{}]):
			if media.get('type',None) == "photo":
				photo_count += 1
			if media.get('type',None) == "video":
				contains_video = True
		return photo_count,contains_video
	def mostEngagedUsers(self, user,num_users, percent, n=-1):
		tweets = self.getAllTweets(user)
		if len(tweets) == 0:
			return {}
		account_d = np.array([])
		top_users = []
		for i in range(0,len(tweets)):
			accounts = []
			if n != -1:
				print(str(n) + " users done, " + str(i) + " tweets in of " + str(len(tweets)))
			if(tweets[i].retweets > 0):
				print(tweets[i].retweets)
				accounts = self.getRetweeters(tweets[i].IDstr)
				print(accounts)
			else:
				print("No retweets")
			for account in accounts:
				account_d = np.append(account_d, account)
		unique_elements, frequency = np.unique(account_d, return_counts=True)
		sorted_indexes = np.argsort(frequency)[::-1]
		sorted_freq = np.sort(frequency)[::-1]
		sorted_by_freq = unique_elements[sorted_indexes]
		ret = min(int(sorted_by_freq.size*percent), num_users)
		return sorted_by_freq[:ret], sorted_freq[:ret]
	
	
	# f= open("retweeterIDs.txt","w+")
	# def writeToFile(list):
	#	 for i in range(0,len(list)):
	#		  print(list[i])
	#		  f.write(str(list[i]) + ",")
	#	 f.write("\n")
	# for i in range(0,5):
	#	 try:
	#		 result = api.get_retweeter_ids(hamilton_tweets[i])
	#		 time.sleep(.25)
	#		 writeToFile(result)
	#	 except:
	#		 result = []
		
	# results = api.get_retweeter_ids(hamilton_tweets[4])
	# # result = api.get_retweeter_ids(id)

	# with open("retweeterIDs.txt",'r') as f:
	# account_ids =  f.readlines()
	# #print(twitter_ids)

	# def retrieveUsers(list):
	#	 users = [None]*len(list)
	#	 for i in range(0,len(list)):
	#		 print(list[i])
	#		 response = api.get_user(id = list[i])
	#		 tweets = api.user_timeline(user_id = list[i],count = 3200,include_rts = True)
		
	#		 users[i] = user.User(list[i],response.screen_name,tweets,response.created_at)
			
	#	 return users
	# results = [None] * len(twitter_ids)
	# for i in range(0,len(twitter_ids)):
	#	 results[i] = twitter_ids[i].split(',')
	#	 results[i].remove("\n")
	# retrieveUsers(results[1])
	# # print(results)


		# f.close()



	# f= open("retweeterIDs.txt","w+")
	# def writeToFile(list):
	#	 for i in range(0,len(list)):
	#		  print(list[i])
	#		  f.write(str(list[i]) + ",")
	#	 f.write("\n")
	# for i in range(0,5):
	#	 try:
	#		 result = api.get_retweeter_ids(hamilton_tweets[i])
	#		 time.sleep(.25)
	#		 writeToFile(result)
	#	 except:a list of twitter objects
	#		 result = []
		
	# results = api.get_retweeter_ids(hamilton_tweets[4])
	# # result = api.get_retweeter_ids(id)

	# with open("retweeterIDs.txt",'r') as f:
	# account_ids =  f.readlines()
	# #print(twitter_ids)

	# def retrieveUsers(list):
	#	 users = [None]*len(list)
	#	 for i in range(0,len(list)):
	#		 print(list[i])
	#		 response = api.get_user(id = list[i])
	#		 tweets = api.user_timeline(user_id = list[i],count = 3200,include_rts = True)
		
	#		 users[i] = user.User(list[i],response.screen_name,tweets,response.created_at)
			
	#	 return users
	# results = [None] * len(twitter_ids)
	# for i in range(0,len(twitter_ids)):
	#	 results[i] = twitter_ids[i].split(',')
	#	 results[i].remove("\n")
	# retrieveUsers(results[1])
	# # print(results)


		# f.close()

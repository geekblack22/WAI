import tweepy
import time
import database
from timeit import default_timer as timer
from collections import Counter
class TwitterInterface:

	"""This class interfaces with the Twitter API"""

	def __init__(self,consumer_key,consumer_secret,bearer_token):
		self.consumer_key = consumer_key
		self.consumer_secret = consumer_secret
		self._auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
		self.api = tweepy.API(self._auth)
		self.lastQ = timer()
		self._bearer_token = bearer_token
		self.client = tweepy.Client(bearer_token=self._bearer_token)

	def storeRetweeters(self,loc,twitter_ids):
		"""Stores the retweeter user IDs in a text file
		Parameters
		----------
		loc: str
			path of text file to save retweeter user IDs to
		twitter_ids: list of str
			list of Status IDs	

		
		 """
		f= open(loc,"w+")
		def writeToFile(list):
			for i in range(0,len(list)):
				print(list[i])
			
				f.write(str(list[i]) + ",")
			f.write("\n")
		for i in range(0,5):
			try:
				result = self.api.get_retweeter_ids(twitter_ids[i])
				time.sleep(.25)
				writeToFile(result)
			except:
				result = []
		f.close()

	def getRetweeters(self, twitter_id):
		self.rateLim()
		print(twitter_id)
		return self.api.get_retweeter_ids(twitter_id)


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
			tweets =  self.getAllTweets(list[i],response.screen_name)
			users[i] = database.User(list[i],response.screen_name,tweets,response.created_at)
		return users

	def getAllTweets(self,id,screen_name):
		"""gets all the tweets of a user  
		Parameters
		----------
		id: str 
			User ID assigned by Twitter 	
		screen_name: str 
			User screen nmae	
		Returns
		-------
		list
			a list of twitter objects
		 """
		self.rateLim()
		tweets = tweepy.Cursor(self.api.user_timeline, user_id = id).items(5)
		user_tweets = []
		for tweet in tweets:
			photo_count, contains_video = self._numMedia(tweet)
			creation_date = tweet.created_at
			hashtags = tweet.entities.get("hashtags")
			tweet_id = tweet.id
			tweet_id_str = tweet.id_str
			tweet_object = database.Tweet(tweet_id,tweet_id_str,screen_name,list_of_hashtags= hashtags,time=creation_date,contains_videos = contains_video,num_photos= photo_count)
			user_tweets.append(tweet_object)
		return user_tweets

	def rateLim(self):
		now = timer()
		if (.34 - (now - self.lastQ) > 0):
			time.sleep(.34 - (now - self.lastQ))
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
	def mostEngagedUsers(self, user,num_users,likes):
		tweets = user.tweets
		account_dict = {}
		top_users = []

		for i in range(0,len(tweets)):
			if likes:
				self.rateLim()
				accounts = self.client.get_liking_users(tweets[i].IDstr)
			else:
				self.rateLim()
				accounts = self.getRetweeters(tweets[i].IDstr)
			for j in range(0,len(accounts)):
				if accounts[j] in account_dict:
					account_dict[accounts[j]] += 1
				else:
					account_dict[accounts[j]] = 1
		k = Counter(account_dict)
 
			# Finding 3 highest values
		high = k.most_common(num_users)

		for i in high:
			top_users[i] = i[0]
		return top_users
	
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

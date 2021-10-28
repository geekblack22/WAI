import tweepy
import time
import database
from timeit import default_timer as timer
class TwitterInterface:

	"""This class interfaces with the Twitter API"""

	def __init__(self,consumer_key,consumer_secret):
		self.consumer_key = consumer_key
		self.consumer_secret = consumer_secret
		self._auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
		self.api = tweepy.API(self._auth)
		self.lastQ = timer()


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
			hashtags = ",".join(hashtags)
			# tweet_id = tweet.id
			tweet_id_str = tweet.id_str
			tweet_object = database.Tweet(tweet_id_str,screen_name,list_of_hashtags= hashtags,time=creation_date,contains_videos = contains_video,num_photos= photo_count)
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
	
	def getEngagers(self,user):
		tweets = user.tweets
		retweeter_dict = {}
		retweeters =  [None]*len(tweets)

		self.api.get_liking_users()
		#for k in range (0, len(tweets)):
			
		for i in range(0,len(tweets)):
			retweeters[i] = self.getRetweeters(tweets[i].IDstr)
			for j in range(0,len(retweeters[i])):
				if i > 0:
					if retweeters[i][j] in retweeters[i-1]:
						print("333")
					


		return num_retweets
	#TODO create function that looks trough tweet history  of a user and created a dictionary of retweeters and how many times they retweet

	
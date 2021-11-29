from networkx.generators import line
import tweepy
import numpy as np
import sys
import os
import time
import database
import datetime
from dateutil.relativedelta import relativedelta
from timeit import default_timer as timer
from collections import Counter
from itertools import islice
import requests
import snscrape.modules.twitter as sntwitter
import json
from dateutil import parser
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
	def scrapeAllTweets(self,user_id,num_tweets=0,user_info = None):
		"""scapes all the tweets of a user  
		Parameters
		----------
		user_id: str 
			(required)User ID assigned by Twitter
		num_tweets: int
			number of tweets to scrapes
		user_info: TwitterUserScraper
			contains all the info scraped from a user
		Returns
		-------
		list
			a list of twitter objects
		 """
		tweets = []
		hashtags = ""
		if user_info is None:
			user_info = enumerate(sntwitter.TwitterUserScraper(str(user_id), isUserId = True).get_items())
		for i,tweet in user_info:
			if num_tweets > 0 and i > num_tweets:
				break
			photo_count, contains_video = self.scrapeMedia(tweet)
			if tweet.hashtags is not None:
				hashtags = ",".join(tweet.hashtags)
			tweets.append(
			database.Tweet(str(tweet.id),
			retweets=tweet.retweetCount,
			time = tweet.date,contains_video = contains_video, 
			num_photos= photo_count,
			list_of_hashtags= hashtags,
			mentioned_ids = self.getMentionedIDs(tweet.mentionedUsers))
			)
		profile_info = enumerate(sntwitter.TwitterProfileScraper(str(user_id), isUserId = True).get_items())
		for i,tweet in profile_info:
			if num_tweets > 0 and i > num_tweets:
				break
			retweet = tweet.retweetedTweet
			if not (retweet is None):
				photo_count,contains_video = self.scrapeMedia(retweet)
				if not (retweet.hashtags  is None):
					hashtags = ",".join(retweet.hashtags)
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
		"""Gets the user IDs of mentioned users
		   Parameters
		   ----------
		   mentions: mentionedUsers
		   		A list of mentioned user objects
		   Returns
		   -------
		   list
		   		A list of user IDs
		"""
		return [user.id for user in mentions] if mentions is not None else []

	def scrapeMedia(self,tweet):
		"""determines the media in a tweet 
		Parameters
		----------
		tweet: Tweet object
			Tweet object in the library snscrape 	
		
		Returns
		-------
		int
			the number of photos in the tweet
		boolean
			if there are any videos in the tweet
		 """
		contains_video = False
		photo_count = 0
		if tweet.media is not None:
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
	def scrapeUserData(self,user_id,get_tweets=True):
		"""Gets all the information pertaining to a use
		----------
		user_id: str
			account ID	
		Returns
		-------
		list
			a user object
		 """
		User = None
		user_data = enumerate(sntwitter.TwitterUserScraper(str(user_id), isUserId = True).get_items())
		for i,tweet in user_data:
			if i > 0:
				break
			user = tweet.user
			tweets = []
			if get_tweets:
				tweets = self.scrapeAllTweets(user_id,user_info= user_data,num_tweets=50)

			#a_month = relativedelta(months=1)
			#a_year  = relativedelta(years = 1)
			#i = 0
			buckets = [0 for i in range(48)]
			#back = datetime.date.today() - a_year
			#back_tmp = back
			#for date in self.getTweetDatesBetween(user.username, database.dtto(back), database.dtto(datetime.datetime.now())):
				#buckets[i] += 1
				#if date >= back_tmp:
					#back += a_month
					#if i%2 == 0:
						#back_tmp = back + datetime.timedelta(days = 15)
					#i += 1
			#buckets = [n/user.statusesCount for n in buckets]
			User = database.User(user_id,tweets,user.created,user.followersCount,user.statusesCount,fingerprint = buckets)
		return User

	def scrapeUsername(self,id):
		user_data = enumerate(sntwitter.TwitterUserScraper(str(id), isUserId = True).get_items())
		user = None
		for i,tweet in user_data:
			if i > 0:
				break
			user = tweet.user
		if user == None:
			return "\\NA\\"
		else:
			return user.username

	def getNumberOfTweetsBetween(self, username, startDate, endDate):
		return int(os.popen("snscrape --jsonl twitter-search 'from:{} since:{} until:{}' | wc -l".format(username, startDate, endDate)).read())
		

	def getTweetDatesBetween(self, username, startDate, endDate):
		print(f"snscrape --jsonl twitter-search 'from:{username} since:{startDate} until:{endDate}' | awk '{{print $6}}' | cut -d T -f1 | cut -c 4-")
		lines = os.popen(f"snscrape --jsonl twitter-search 'from:{username} since:{startDate} until:{endDate}' | awk '{{print $6}}' | cut -d T -f1 | cut -c 4-").readlines()

		return [datetime.datetime.strptime(line, "%y-%m-%d\n").date() for line in lines][::-1]
	def getTweetsBetween(self, username, startDate, endDate):
		# print(f"snscrape --jsonl twitter-search 'from:{username} since:{startDate} until:{endDate}'")
		tweet_objects = []
		try:
			print("starting tweets pull for "+str(username))
			print(f"snscrape --jsonl twitter-search 'from:{username} since:{startDate} until:{endDate}'")
			
			lines = os.popen(f"snscrape --jsonl twitter-search 'from:{username} since:{startDate} until:{endDate}'").readlines()
			tweets = [json.loads(line) for line in lines]
			print("finished tweets pull")

			for tweet in tweets:
				hashtags = ""
						
				if tweet["hashtags"] != None:
					hashtags =  ",".join(tweet["hashtags"])
				date = datetime.datetime.fromisoformat(tweet["date"])

				date = date.strftime("%Y-%m-%d %I:%M%p")
				print(date)
				tweet_objects.append(database.Tweet(tweet["id"],retweets= tweet["retweetCount"],list_of_hashtags=hashtags,posterID= tweet["user"]["id"],time = date))
		except:
			print("Error user data not found")
		return tweet_objects


	def getAllTweets(self,id,num = 50):
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

		tweets = tweepy.Cursor(self.api.user_timeline,include_rts=False,user_id = id).items(num)

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

		"""determines the media in a tweet 
		Parameters
		----------
		user: str
			User ID
		num_users: int
			Number of users to return
		percent: float
			Top percentage of users ID's to return based on number of retweets
		n: int
			Number of seed users done
		Returns
		-------
		list
			User IDs of top n percent of users based on retweets

		
		 """

		tweets = self.getAllTweets(user,num=400)

		if len(tweets) == 0:
			return {}
		account_d = np.array([],dtype = 'object')
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
	
	

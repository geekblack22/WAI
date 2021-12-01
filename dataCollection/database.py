#TODO: Create helper functions to access sql database base on specified criteria
import datetime
import heapq
import pyodbc 
import itertools
import string
import re
import numpy as np
class Database:
	
	def __init__(self, server, database,uid,pwd):
		self.db = pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server};"
			"Server=" + server + ";"+
			"Database=" + database + ";"+
			"UID=" + uid + ";"+
			"PWD=" + pwd + ";")
		self.cursor = self.db.cursor()

	def viewAll(self):
		for row in self.cursor.tables():
			print(r)

	#def getAllTweets(self):
		#lst = self.cursor.execute("SELECT TOP (100) [TweetID],[idStr],[screenName],[retweetCount],[createdAt] FROM [dbo].[Tweet]")
		#tweets = [Tweet(row[0],row[1],row[2],row[3] if row[3] is not None else 0, row[4]) for row in lst]
		#return tweets

	def getAllTweetsBetween(self,start,end):
		lst = self.cursor.execute("SELECT [IDStr],[containsVideo],[numberOfPictures],[listOfHashtags],[time],[posterID],[retweets]  FROM [dbo].[Tweets] WHERE [time] BETWEEN " + dtto(start) + " AND " + dtto(end))
		tweets = [Tweet(row[0],list_of_hashtags= row[3],time = row[4],posterID= row[5],retweets= row[6]) for row in lst]
		return tweets

	def getAllTweetsByUser(self, screenName):
		lst = self.cursor.execute("SELECT [screenName],[retweetCount],[createdAt] FROM [dbo].[Tweet] WHERE [screenName] = '" + screenName + "'")
		tweets = [Tweet(row[0],row[1],row[2],row[3] if row[3] is not None else 0, row[4]) for row in lst]
		return tweets
	def getAllTweets(self):
		lst = self.cursor.execute("SELECT [IDStr],[containsVideo],[numberOfPictures],[listOfHashtags],[time],[posterID],[retweets] FROM [dbo].[Tweets]")
		tweets = [Tweet(row[0],contains_video=row[1],num_photos=row[2],list_of_hashtags=row[3],time=row[4],posterID=row[5], retweets=row[6]) for row in lst]
		return tweets
	def getAllTweetsByUserID(self, id):
		lst = self.cursor.execute("SELECT [IDStr],[containsVideo],[numberOfPictures],[listOfHashtags],[time],[posterID],[retweets] FROM [dbo].[Tweets] WHERE [posterID] = '" + id + "'")
		tweets = [Tweet(row[0],contains_video=row[1],num_photos=row[2],list_of_hashtags=row[3],time=row[4],posterID=row[5], retweets=row[6]) for row in lst]
		return tweets
	def getAllTweetsBetweenByUserID(self, ids,start,end):
		placeholders = ", ".join(["?"] * len(ids))
		lst = self.cursor.execute("SELECT [IDStr],[containsVideo],[numberOfPictures],[listOfHashtags],[time],[posterID],[retweets] FROM [dbo].[Tweets] WHERE [posterID] IN (""" + placeholders + ")"+" AND [time] BETWEEN " + dtto(start) + " AND " + dtto(end),ids)
		tweets = [Tweet(row[0],list_of_hashtags= row[3],time = row[4],posterID= row[5],retweets= row[6]) for row in lst]	
		return tweets

	def checkForDuplicateTweets(self):
		lst = self.cursor.execute("SELECT [IDStr],COUNT(*) FROM [dbo].[Tweets] GROUP BY  [IDStr] HAVING COUNT(*) > 1;")
		tweets = [row[0] for row in lst]
		print(len(tweets))
		#print(tweets)
	def seenSeed(self, idstr):
		print(idstr)
		lst = self.cursor.execute("""SELECT [ID] FROM [dbo].[User] WHERE [engagementUsers] LIKE '{}'""".format("%" + idstr + "%"))
		try:
			usr = next(lst)
			return True
		except:
			return False

	def highestPercentGrowth(self, n, date):
		date = dtto(date)
		lst = self.cursor.execute("SELECT [idStr] ,Min([followerCount]) as minFollowers, Max(followerCount) as maxFollowers, 100*(Max(followerCount)-Min([followerCount]))/(1+Max(followerCount)) percentChange FROM [dbo].[V_Handles_History] WHERE [snapshotDate] >= DATEADD(day, -30, {}) AND [snapshotDate] <= {} AND country in ('ch','ru','ir') group by idStr order by percentChange desc".format(date,date))
		return [row[0] for row in itertools.islice(lst,n)]

	def insertUser(self,user):
		self.cursor.execute("""INSERT INTO [dbo].[User] ([IDStr],[creationDate],[engagementAmount],[engagementUsers],[numberOfFollowers],[numberOfTweets],[fingerprint]) VALUES(?,?,?,?,?,?,?)""",
		(user.IDstr,user.creationDate,str([i[0] for i in user.engagement])[1:-1],str([int(i[1]) for i in user.engagement])[1:-1],user.follower_count,user.tweet_count,str(user.fingerprint)[1:-1])
		)
		user.ID = self.cursor.execute("SELECT SCOPE_IDENTITY() AS [SCOPE_IDENTITY];")
		return user
	def getAllUsers(self):
		lst = self.cursor.execute("""SELECT [ID],[creationDate],[engagementAmount],[engagementUsers],[numberOfFollowers],[numberOfTweets],[fingerprint],[IDStr] FROM [dbo].[User]""")
		return [User(usr[7], [], usr[1], usr[4], usr[5], ID = usr[0], engagement = [(int(n), int(user)) for n,user in zip(usr[2].split(","),usr[3].split(","))],fingerprint = [float(n) for n in usr[6].split(",")]) for usr in lst]
	
	def clean(self):
		users = self.getAllUsers()
		for user in users:
			print(user.getFingerprint())

	def getUsertp(self, idStr):
		lst = self.cursor.execute("""SELECT [ID],[creationDate],[engagementAmount],[engagementUsers],[numberOfFollowers],[numberOfTweets],[fingerprint] FROM [dbo].[User] WHERE [IDStr] = ?""",(idStr))
		usr = None
		try:
			usr = next(lst)
		except:
			if usr is None:
				return None
		return User(idStr, [], usr[1], usr[4], usr[5], ID = usr[0], engagement = [(int(n), int(user)) for n,user in zip(usr[2].split(","),usr[3].split(","))],fingerprint = [float(n) for n in usr[6].split(",")])

	def getUsername(self,user_id):
		self.cursor.execute("""SELECT [screenName] FROM [dbo].[Handle] WHERE [IDStr] = ?""",(user_id))
		result =  self.cursor.fetchall()
		user_name = str(result[0])
		user_name = user_name.translate(str.maketrans('','', "(),'"))
		return user_name.strip()
	def getCountry(self,user_id):
		self.cursor.execute("""SELECT [country] FROM [dbo].[Handle] WHERE [IDStr] = ?""",(user_id))
		result =  self.cursor.fetchall()
		country= str(result[0])
		country = country.translate(str.maketrans('','', "(),'"))
		return country.strip()

	def updateUser(self,user):
		self.cursor.execute("""UPDATE [dbo].[User] SET [IDstr] = ?, [creationDate] = ?, [numberOfFollowers] = ?, [numberOfTweets] = ?, [engagementAmount] = ?, [engagementUsers] = ?, [fingerprint] = ? WHERE [ID] = ?""",(user.IDstr, user.creationDate, user.follower_count, user.tweet_count, str([i[0] for i in user.engagement])[1:-1], str([i[1] for i in user.engagement])[1:-1],str(user.fingerprint)[1:-1], user.ID))
	def updateUserTweets(self,tweet):
			print(tweet)
			self.cursor.execute("""UPDATE [dbo].[Tweets] SET [time] = ? WHERE [IDStr] = ?""",tweet.time,tweet.IDstr)
	def insertTweet(self,tweet):
		print(tweet)
		self.cursor.execute("""INSERT INTO [dbo].[Tweets] ([IDStr],[containsVideo],[numberOfPictures],[listOfHashtags],[time],[posterID],[retweets]) VALUES(?,?,?,?,?,?,?)""",
		(tweet.IDstr,tweet.contains_video,tweet.num_photos,tweet.list_of_hashtags,tweet.time,str(tweet.posterID).strip(),tweet.retweets)
		)
		tweet.ID = self.cursor.execute("SELECT SCOPE_IDENTITY() AS [SCOPE_IDENTITY];")
		return tweet
	def getAllEUsers(self):
		lst = self.cursor.execute("""SELECT * FROM [dbo].[secondaryUsers]""")
		return lst
	def dup(self):
		lst = self.cursor.execute("""SELECT * FROM [dbo].[secondaryUsers] WHERE ID IN ( SELECT MAX(ID) AS MaxRecordID FROM [dbo].[secondaryUsers] GROUP BY [ID]);""")
		return [row for row in lst]
	def getInfo(self, ID):
		lst = self.cursor.execute("""SELECT * FROM [dbo].[secondaryUsers] WHERE [ID] = ?""", (ID))
		try:
			return next(lst)
		except:
			return None

	def addInfo(self, ID, matches, cap, ir, ch, ru):
		self.cursor.execute("SET IDENTITY_INSERT [dbo].[secondaryUsers] ON")
		self.cursor.execute("""INSERT INTO [dbo].[secondaryUsers] ([ID],[iran],[china],[russia],[unameM],[cap]) VALUES(?,?,?,?,?,?)""",
		(ID,ir,ch,ru,1 if matches else 0,cap)
		)
		self.cursor.execute("SET IDENTITY_INSERT [dbo].[secondaryUsers] OFF")
		
	#def clear(self):
		#self.cursor.execute("""Delete From [dbo].[Tweets];""")
		#self.db.commit()
	def userTweetTable(self):
		lst = self.cursor.execute("Select [posterID], string_agg(cast([time] as NVARCHAR(MAX)),',') as dates from [dbo].[tweets] Group by [posterID]")
		return [row for row in lst]
			
	#def userTweetTable(self):
		#tweets = self.getAllTweets()
		#table = {}
		#for tweet in tweets:
			#if tweet.posterID in table:
				#table[tweet.posterID].append(tweet)
			#else:
				#table[tweet.posterID] = [tweet]
		#return table
			
		
	# def clear(self):
	# 	self.cursor.execute("""Delete From [dbo].[Tweets];""")
	# 	self.db.commit()
	def updateTweet(self,tweet):
		self.cursor.execute("""UPDATE [dbo].[Tweets] SET [IDStr] = ?, [containsVideo] = ?, [numberOfPictures] = ?, [listOfHashtags] = ?, [time] = ?, [posterID] = ?, [retweets] = ? WHERE [ID] = ? """,
		(tweet.IDstr,tweet.contains_video,tweet.num_photos,tweet.list_of_hashtags,tweet.time,str(tweet.posterID).strip(),tweet.retweets,tweet.ID)
		)
		tweet.ID = self.cursor.execute("SELECT SCOPE_IDENTITY() AS [SCOPE_IDENTITY];")
		return tweet
	def removeDuplicate(self):
		self.cursor.execute("DELETE FROM [dbo].[Tweets] WHERE id NOT IN ( SELECT MIN(id) FROM Tweets GROUP BY [IDStr]);")
		self.db.commit()
	def getHastagDates(self,hashtag,tweets):
		return [tweet.time for tweet in tweets if(hashtag in tweet.list_of_hashtags)]
	def hashtagProportions(self,ids,start,end):
		tweets = self.getAllTweetsBetweenByUserID(ids,start,end)
		hashtags = [tweet.list_of_hashtags.split(",") for tweet in tweets  if (tweet.list_of_hashtags != "")]		
		hashtags = [item for sublist in hashtags for item in sublist]
		hashtags = [hashtag for hashtag in hashtags if hashtag.count('?')/float(len(hashtag)) < .4]
		unique_elements, frequency = np.unique(hashtags, return_counts=True)
		sorted_indexes = np.argsort(frequency)[::-1]
		
		sorted_by_freq = unique_elements[sorted_indexes]
		sorted_freq = np.sort(frequency)[::-1]
		ret = min(int(sorted_by_freq.size*.05),20)

		#percents = [float(freq)/float(len(sorted_by_freq)) * 100 for freq in frequency]
		topHashtags = sorted_by_freq[:ret]
		topHashtagsFreq = sorted_freq[:ret]
		dates = [self.getHastagDates(hashtag,tweets) for hashtag in topHashtags]
		return 	topHashtags, topHashtagsFreq,dates

def dtto(t):
	return "'" + str(t).split(' ')[0] + "'"
class Tweet:
	def __init__(self, IDstr, ID = 0,retweets=0, time=0, contains_video=False, num_photos=0,list_of_hashtags="",posterID="",mentioned_ids=[],isRetweet = False):
		self.ID = ID
		self.IDstr = IDstr	   #string
		self.posterID = posterID
		self.retweets = retweets
		self.time = time
		self.contains_video = contains_video
		self.list_of_hashtags = list_of_hashtags
		self.mentioned_ids = mentioned_ids
		self.num_photos = num_photos
		self.isRetweet = isRetweet
	def __str__(self):
		content = ( "TweetID: "+ str(self.IDstr)
		+" posterID: "+ str(self.posterID)
		+" retweets: "+str(self.retweets)
		+" time: " + str(self.time)
		+" contains_video: " + str(self.contains_video)
		+" list_of_hashtags: " + str(self.list_of_hashtags)
		+" num_photos: "  + str(self.num_photos)
		+" mentioned_ids: " + str(self.mentioned_ids)
		+" isRetweet: " + str(self.isRetweet))
		return content

def retweet_compare(tweet1, tweet2):
	return tweet1.retweets - tweet2.retweets
class User:
	def __init__(self, IDstr, tweets,creationDate, follower_count,tweet_count,ID=0,engagement=[],fingerprint=[]):	
		self.ID = ID
		self.IDstr = IDstr	   #string
		self.tweets = tweets
		self.creationDate = creationDate	#dateTime
		self.follower_count = follower_count
		self.tweet_count = tweet_count
		self.engagement = engagement
		self.fingerprint = fingerprint
		self.countries = None
	def getFingerprint(self):
		thisyear = sum(self.fingerprint)
		if thisyear == 0.0:	
			return self.fingerprint[0:25]
		return [(1 / thisyear) * bucket for bucket in self.fingerprint][0:25]
	def getCountries(self,db):
		if self.countries != None:
			return self.countries
		ret  = {'ru':0,'ch':0,'ir':0} 
		for item in self.engagement:
			s = str(item[1])
			s = s + " "*(20-len(s))
			ret[db.getCountry(s)] += 1
		self.countries = ret
		return ret
	def mod(self,lod):
		time = datetime.datetime(2020,11,17,0,0,0)
		lod.sort()
		buckets = [0.0]*48
		ind = 0
		for i in range(48):
			amount = 0
			while lod[ind] < time.time():
				amount += 1
				ind += 1
				if ind >= len(lod):
					break
			if ind >= len(lod):
				break
			buckets[i] = amount/len(lod)
			time += datetime.timedelta(minutes = 30)
		return buckets
	def fineFingerPrint(self,db):
		if len(self.fingerprint) == 365:
			return self.fingerprint
		tweets = db.getAllTweetsByUserID(self.IDstr)
		if len(tweets) == 0:
			return [0.0]*365
		date = datetime.datetime(2020,11,17,0,0,0)
		tweets.sort(key=lambda e : e.time)
		buckets = [0.0]*365
		ind = 0
		for i in range(365):
			amount = 0
			while tweets[ind].time < date:
				amount += 1
				ind += 1
				if ind >= len(tweets):
					break
			if ind >= len(tweets):
				break
			buckets[i] = amount/len(tweets)
			date += datetime.timedelta(days = 1)
		return buckets

	def matches(self, username):
		patern = re.compile("^[a-zA-Z_]+[0-9]{3}[0-9]*$")
		return bool(patern.match(username))

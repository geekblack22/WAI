#TODO: Create helper functions to access sql database base on specified criteria
import datetime
import heapq
import pyodbc 
import itertools
import string
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

	def getAllTweets(self):
		lst = self.cursor.execute("SELECT TOP (100) [tweetID],[idStr],[screenName],[retweetCount],[createdAt] FROM [dbo].[Tweet]")
		tweets = [Tweet(row[0],row[1],row[2],row[3] if row[3] is not None else 0, row[4]) for row in lst]
		return tweets

	def getAllTweetsBetween(self,start,end):
		lst = self.cursor.execute("SELECT [tweetID],[idStr],[screenName],[retweetCount],[createdAt] FROM [dbo].[Tweet] WHERE [createdAT] BETWEEN " + dtto(start) + " AND " + dtto(end))
		tweets = [Tweet(row[0],row[1],row[2],row[3] if row[3] is not None else 0, row[4]) for row in lst]
		return tweets

	def getAllTweetsByUser(self, screenName):
		lst = self.cursor.execute("SELECT [tweetID],[idStr],[screenName],[retweetCount],[createdAt] FROM [dbo].[Tweet] WHERE [screenName] = '" + screenName + "'")
		tweets = [Tweet(row[0],row[1],row[2],row[3] if row[3] is not None else 0, row[4]) for row in lst]
		return tweets
	def getAllTweetsByUserID(self, id):
		lst = self.cursor.execute("SELECT [tweetID],[idStr],[screenName],[retweetCount],[createdAt] FROM [dbo].[Tweet] WHERE [idStr] = '" + id + "'")
		tweets = [Tweet(row[0],row[1],row[2],row[3] if row[3] is not None else 0, row[4]) for row in lst]
		return tweets

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
			for i,t in enumerate(user.engagement):
				user.engagement[i] = (t[0], int(''.join(c for c in t[1] if c.isdigit())))
			self.updateUser(user)

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
			
			return user_name

	def updateUser(self,user):
		self.cursor.execute("""UPDATE [dbo].[User] SET [IDstr] = ?, [creationDate] = ?, [numberOfFollowers] = ?, [numberOfTweets] = ?, [engagementAmount] = ?, [engagementUsers] = ?, [fingerprint] = ? WHERE [ID] = ?""",(user.IDstr, user.creationDate, user.follower_count, user.tweet_count, str([i[0] for i in user.engagement])[1:-1], str([i[1] for i in user.engagement])[1:-1],str(user.fingerprint)[1:-1], user.ID))

	def insertTweet(self,tweet):
		print(tweet)
		self.cursor.execute("""INSERT INTO [dbo].[Tweets] ([IDStr],[containsVideo],[numberOfPictures],[listOfHashtags],[time],[posterID],[retweets]) VALUES(?,?,?,?,?,?,?)""",
		(tweet.IDstr,tweet.contains_video,tweet.num_photos,tweet.list_of_hashtags,tweet.time,str(tweet.posterID).strip(),tweet.retweets)
		)
		tweet.ID = self.cursor.execute("SELECT SCOPE_IDENTITY() AS [SCOPE_IDENTITY];")
		return tweet
	def clear(self):
		self.cursor.execute("""Delete From [dbo].[User];""")
		self.cursor.execute("""Delete From [dbo].[Tweets];""")
		self.db.commit()
	def updateTweet(self,tweet):
		self.cursor.execute("""UPDATE [dbo].[Tweets] SET [IDStr] = ?, [containsVideo] = ?, [numberOfPictures] = ?, [listOfHashtags] = ?, [time] = ?, [posterID] = ?, [retweets] = ? WHERE [ID] = ? """,
		(tweet.IDstr,tweet.contains_video,tweet.num_photos,tweet.list_of_hashtags,tweet.time,str(tweet.posterID).strip(),tweet.retweets,tweet.ID)
		)
		tweet.ID = self.cursor.execute("SELECT SCOPE_IDENTITY() AS [SCOPE_IDENTITY];")
		return tweet
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
	def getFingerprint(self):
        thisyear = sum(self.fingerprint) * self.tweet_count
        return [(self.tweet_count / thisyear) * bucket for bucket in self.fingerprint]

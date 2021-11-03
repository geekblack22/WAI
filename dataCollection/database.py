#TODO: Create helper functions to access sql database base on specified criteria
import datetime
import heapq
import pyodbc 
import itertools

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

	def highestPercentGrowth(self, n, date):
		date = dtto(date)
		lst = self.cursor.execute("SELECT [idStr] ,Min([followerCount]) as minFollowers, Max(followerCount) as maxFollowers, 100*(Max(followerCount)-Min([followerCount]))/(1+Max(followerCount)) percentChange FROM [dbo].[V_Handles_History] WHERE [snapshotDate] >= DATEADD(day, -30, {}) AND [snapshotDate] <= {} AND country in ('ch','ru','ir') group by idStr order by percentChange desc".format(date,date))
		return [row[0] for row in itertools.islice(lst,n)]

	def insertUser(self,user):
		self.cursor.execute("""INSERT INTO [dbo].[Users] ([IDStr],[creationDate]) VALUES(?,?)""",
		(user.IDstr,user.creationDate)
		)
		user.ID = self.cursor.execute("SELECT SCOPE_IDENTITY() AS [SCOPE_IDENTITY];")
		return user
	def instertListofUsers(self,users):
		for i in range(0,len(users)):
			self.insertUser(users[i])
	def insertTweet(self,tweet):
		self.cursor.execute("""INSERT INTO [dbo].[Tweet] ([IDStr],[containsVideo],[numberOfPictures],[listOfHashtags],[time],[posterID],[retweets]) VALUES(?,?,?,?,?,?,?)""",
		(tweet.IDstr,tweet.contains_videos,tweet.num_photos,tweet.list_of_hashtags,tweet.time,tweet.posterID,tweet.retweets)
		)
		tweet.ID = self.cursor.execute("SELECT SCOPE_IDENTITY() AS [SCOPE_IDENTITY];")
		return tweet
	def instertListofTweets(self,tweets):
		for i in range(0,len(tweets)):
			self.insertTweet(tweets[i])
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
	def __init__(self, IDstr, tweets,creationDate, ID=0):	
		self.ID = ID
		self.IDstr = IDstr	   #string
		self.tweets = tweets
		self.creationDate = creationDate	#dateTime

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

	def highestPercentGrowth(self, n, date):
		date = dtto(date)
		lst = self.cursor.execute("SELECT [screenName] ,Min([followerCount]) as minFollowers, Max(followerCount) as maxFollowers, 100*(Max(followerCount)-Min([followerCount]))/(1+Max(followerCount)) percentChange FROM [dbo].[V_Handles_History] WHERE [snapshotDate] >= DATEADD(day, -30, {}) AND [snapshotDate] <= {} AND country in ('ch','ru','ir') group by screenName order by percentChange desc".format(date,date))
		return [row[0] for row in itertools.islice(lst,n)]

	def insertUser(self,user):
		self.cursor.execute("""INSERT INTO [dbo].[Users] ([IDStr],[creationDate]) VALUES(?,?)""",
		(user.IDstr,user.creationDate)
		)
	def instertListofUsers(self,users):
		for i in range(0,len(users)):
			self.insertUser(users[i])
	def insertTweet(self,tweet):
		self.cursor.execute("""INSERT INTO [dbo].[Tweet] ([IDStr],[containsVideo],[numberOfPictures],[listOfHashtags],[time],[posterID],[retweets]) VALUES(?,?,?,?,?,?,?)""",
		(tweet.IDstr,tweet.contains_videos,tweet.num_photos,tweet.list_of_hashtags,tweet.time,tweet.posterID,tweet.retweets)
		)
	def instertListofTweets(self,tweets):
		for i in range(0,len(tweets)):
			self.insertTweet(tweets[i])
def dtto(t):
	return "'" + str(t).split(' ')[0] + "'"
class Tweet:
	def __init__(self, ID, IDstr, screenName, retweets=0, time=0, contains_videos=False, num_photos=0,list_of_hashtags=[],posterID=""):
		self.ID = ID		  #int
		self.IDstr = IDstr	   #string
		self.posterID = posterID
		self.retweets = retweets
		self.time = time
		self.contains_videos = contains_videos
		self.list_of_hashtags = list_of_hashtags
		self.screenName = screenName
		self.num_photos = num_photos

def retweet_compare(tweet1, tweet2):
	return tweet1.retweets - tweet2.retweets
class User:
	def __init__(self, IDstr, screenName, tweets,creationDate, ID=0):
		self.ID = ID		  #int
		self.IDstr = IDstr	   #string
		self.screenName = screenName #string
		self.tweets = tweets
		self.creationDate = creationDate	#dateTime
#TODO: Create helper functions to access sql database base on specified criteria
import datetime
import heapq
import pyodbc 

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
		lst = self.cursor.execute("SELECT [tweetID],[idStr],[screenName],[retweetCount],[createdAt] FROM [dbo].[Tweet] WHERE [screenName] = ''" + screenName + "''")
		tweets = [Tweet(row[0],row[1],row[2],row[3] if row[3] is not None else 0, row[4]) for row in lst]
		return tweets

	def highestPercentGrowth(self, n):
		# get all users
		lst = self.cursor.execute("SELECT [id],[screenName] FROM [dbo].[V_Handle_History]")
		nameSet = {}
		ret = []
		heapq.heapify(ret)
		# count how many times each screenName appears
		for row in lst:
			if row[1] in nameSet:
				nameSet[row[1]] += 1
			else:
				nameSet[row[1]] = 1
		# for each screenName find the earliest row and latest row
		for key, value in nameSet:
			# skip if only 1 row
			if value == 1:
				continue
			else:
				lst_name = self.cursor.execute("SELECT [id],[screenName],[snapshotDate],[followerCount] FROM [dbo].[V_Handle_History] WHERE [screenName] [screenName] = ''"  + key + "''")
				min = lst_name[0]
				max = lst_name[0]
				for row in lst_name:
					if row[2] > max[2]:
						max = row
					if row[2] < min[2]:
						min = row
				users = self.cursor.execute("SELECT [id],[idStr],[screenName],[createdAt] FROM [dbo].[Handle] WHERE [screenName] = ''" + key + "''")
				tweets = self.getAllTweetsByUser(key)
				adding = User(users[0][0], users[0][1], users[0][2],tweets, users[0][3])
				heapq.heappush(ret, ((max[3] - min[3]).total_seconds())/min[3].total_seconds(), adding)
		return heapq.nlargest(ret,n)

	def insertUser(self,user):
		self.cursor.execute("""INSERT INTO [dbo].[User] ([IDStr],[creationDate]) VALUES(?,?)""",
		(user.IDstr,user.creationDate)
		)
		self.db.commit()
	def instertListofUsers(self,users):
		for i in range(0,len(users)):
			self.insertUser(users[i])
	def insertTweet(self,tweet):
		self.cursor.execute("""INSERT INTO  [dbo].[Tweets] ([IDStr],[containsVideo],[numberOfPictures],[listOfHashtags],[time],[posterID],[retweets]) VALUES(?,?,?,?,?,?,?)""",
		(tweet.IDstr,tweet.contains_videos,tweet.num_photos,tweet.list_of_hashtags,tweet.time,tweet.posterID,tweet.retweets)
		)
		self.db.commit()
	def instertListofTweets(self,tweets):
		for i in range(0,len(tweets)):
			self.insertTweet(tweets[i])
def dtto(t):
	return "'" + str(t).split(' ')[0] + "'"
class Tweet:
	def __init__(self, ID, IDstr, screenName, retweets=0, time=0, contains_videos=False, num_photos=0,list_of_hashtags="",posterID=""):
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
	def __init__(self,IDstr, screenName, tweets,creationDate):
		self.IDstr = IDstr	   #string
		self.screenName = screenName #string
		self.tweets = tweets
		self.creationDate = creationDate	#dateTime

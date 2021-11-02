import snscrape.modules.twitter as sntwitter
import pandas as pd

tweets_list1 = []

mediums = []
contains_video = []
count = 0
# Using TwitterSearchScraper to scrape data and append tweets to list
for i,tweet in enumerate(sntwitter.TwitterUserScraper('2318647908', isUserId = True).get_items()):
    if i>200:
        break
    print(tweet.mentionedUsers)
    tweets_list1.append([tweet.date, tweet.id, tweet.content, tweet.user.username])
    if not (tweet.media is None):
        for medium in tweet.media:
            if isinstance(medium, sntwitter.Photo):
                count+=1
            contains_video.append((isinstance(medium, sntwitter.Video)) or isinstance(medium, sntwitter.VideoVariant))

            
        


           
 

    
print(contains_video)
# print(tweets_df1.Tweet_ID.tolist())

import json
import numpy as np
from datetime import datetime

class Tweet:
    """
    Original corpus data as an object
    """

    def __init__(self, id, title, description, doc_date, likes, retweets, url, hashtags, user_followers, user_followed, user_verified, user_tweets ):
        self.id = id
        self.title = title
        self.description = description
        self.doc_date = str(datetime.strptime(doc_date, "%a %b %d %H:%M:%S %z %Y"))
        self.likes = likes
        self.retweets = retweets
        self.url = url
        self.hashtags = hashtags
        self.user_followers = user_followers
        self.user_followed = user_followed
        self.user_verified = user_verified
        self.user_tweets = user_tweets

    def to_json(self):
        return self.__dict__
    
    def getCustomScore(self):
        verifiedCount = 0
        if self.user_verified:
            verifiedCount = 1
        
        return self.retweets * 2 + self.likes + ((np.log(self.user_followers+1)/np.log(max(10,self.user_followed)))) + verifiedCount + (1/self.user_tweets)

    def __str__(self):
        """
        Print the object content as a JSON string
        """
        return json.dumps(self)


class StatsDocument:
    """
    Original corpus data as an object
    """

    def __init__(self, id, title, description, doc_date, url, count):
        self.id = id
        self.title = title
        self.description = description
        self.doc_date = doc_date
        self.url = url
        self.count = count

    def __str__(self):
        """
        Print the object content as a JSON string
        """
        return json.dumps(self)


class ResultItem:
    def __init__(self, id, title, description, doc_date, url, ranking):
        self.id = id
        self.title = title
        self.description = description
        self.doc_date = doc_date
        self.url = url
        self.ranking = ranking

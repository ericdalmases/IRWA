import numpy as np



def getScore(self):
    #likes, retweets| private, followers, followed, verified
    #1. retweets 2. likes 3. ratio followers/followed 4. verified
    verifiedCount = 0
    if self.user.verified:
      verifiedCount = 1
    #print(f"account: {self.doc_id}, SCORE: {self.retweets * 2 + self.likes + self.num_replies * 1.5 + ((np.log(self.user.followers+1)/np.log(max(10,self.user.followed)))) + verifiedCount + (1/self.user.num_tweets)},  retweets: {self.retweets * 2}, likes: {self.likes}, replies: {self.num_replies * 1.5}, ratio: {(np.log(self.user.followers+1)/np.log(max(10,self.user.followed)))}, verified: {verifiedCount}, num_tweets:{(1/self.user.num_tweets)}")
    return self.retweets * 2 + self.likes + self.num_replies * 1.5 + ((np.log(self.user.followers+1)/np.log(max(10,self.user.followed)))) + verifiedCount + (1/self.user.num_tweets)
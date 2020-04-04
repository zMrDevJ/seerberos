#!usr/bin/python

from quoteAPI import getQuoteOfDay
import tweepy
import time


# Class Bot
class Bot:
    def __init__(self, api):
        self.api = api
        self.user = api.me()

    def postStatus(self, update):
        self.api.update_status(update)
        print('Status updated!')

    # TODO Refactoring
    def postRetweetFromUser(self, user_screen_name, tweetsNo):
        query = f'from:{user_screen_name} -is:retweet -is:reply'
        tweets = tweepy.Cursor(self.api.search, query,
                               tweet_mode='extended').items(tweetsNo)
        for tweet in tweets:
            try:
                tweet.favorite()
                tweet.retweet()
                print(f'Retweeted a tweet from {user_screen_name}!')
                time.sleep(20)
            except tweepy.TweepError as e:
                print(e.reason)
                time.sleep(10)

    def postQuoteOfDay(self):
        quote, author = getQuoteOfDay()
        tweet = f'"{quote.lstrip()}"\n~{author}\n\n#QoD #quoteoftheday #quote #seerberos #feeds'
        try:
            self.postStatus(tweet)
            print('Posted the QoD!')
        except tweepy.TweepError as e:
            print(e.reason)

    def searchHashtags(self, query, tweetsNo, followersCount=500):
        tweets = tweepy.Cursor(self.api.search, query,
                               tweet_mode='extended').items(tweetsNo)
        for tweet in tweets:
            try:
                # A simple account check before retweetting
                if (tweet.user.followers_count >= followersCount):
                    tweet.retweet()
                    print('Retweeted a tweet!')
                    time.sleep(20)
            except tweepy.TweepError as e:
                print(e.reason)
                time.sleep(10)

    def print(self):
        msg = f'Hello, I\'m {self.user.screen_name}!'
        print(msg)
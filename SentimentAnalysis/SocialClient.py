import praw
import pandas as pd
import numpy as np
import re
from textblob import TextBlob
import json
from constants import Constants
from abc import ABC, abstractmethod
path = Constants().get_constant("path")


def get_post_sentiment(post):
    print(post)
    analysis = TextBlob(post)
    if analysis.sentiment.polarity > 0:
        return 1
    elif analysis.sentiment.polarity == 0:
        return 0
    else:
        return -1


def load_configuration(filename = f"{path}/secrets.json"):
    with open(filename, 'r') as file:
        data = json.load(file)

    public_key = data.get('public', "")
    private_secret = data.get('private', "")
    user_agent = data.get('user_agent',"")
    return public_key, private_secret,user_agent

class TextCleaner:
    def clean_text(self, text):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", text).split())

class RedditAdapter:
    def __init__(self, client_id = None, client_secret = None, user_agent = None):
        if client_id == None or client_secret == None or user_agent == None:
            public_key, private_secret, user_agent = load_configuration()
            self.comunicator = praw.Reddit(
                client_id=public_key,
                client_secret=private_secret,
                redirect_uri="http://localhost:8888",
                user_agent=user_agent,
            )
        else:
            self.comunicator = praw.Reddit(
                client_id=client_id,
                client_secret=client_secret,
                user_agent=user_agent
            )

    def get_hot_posts(self, input, limit):
        return self.comunicator.subreddit(input).hot(limit=limit)

class AbstractSocialClient(ABC):
    def __init__(self, adapter: RedditAdapter, text_cleaner=None):
        self.adapter = adapter
        if text_cleaner is None:
            self.text_cleaner = TextCleaner()
        else:
            self.text_cleaner = text_cleaner

    @abstractmethod
    def get_posts(self, input, count=10):
        pass

class SocialClient(AbstractSocialClient):
    def get_posts(self, input, count=10):
        posts = []
        for submission in self.adapter.get_hot_posts(input, limit=count):
            clean_title = self.text_cleaner.clean_text(submission.title)
            posts.append(clean_title)
        return posts


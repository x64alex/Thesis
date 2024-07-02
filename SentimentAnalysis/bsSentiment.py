import sys

from SocialClient import SocialClient, RedditAdapter, get_post_sentiment
from blackscholes import sentiment_analysis_with_stochastic_model

def bsSentiment(companyName):
    adapter = RedditAdapter()
    client = SocialClient(adapter)
    posts = client.get_posts(companyName, 20)

    sentiment = 0

    for i in range(10):
        sentiment_post = 0
        for post in posts:
            sentiment_post += sentiment_analysis_with_stochastic_model(post)    

        sentiment += sentiment_post/len(posts)

    sentiment = sentiment /3
    sentiment *= 10
    if sentiment >=0:
        return f"{sentiment:.2f}% positive"
    return f"{sentiment:.2f}% negative"



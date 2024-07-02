import sys
sys.path.append('./SentimentAnalysis')

from SocialClient import SocialClient, RedditAdapter, get_post_sentiment
from blackscholes import sentiment_analysis_with_stochastic_model

def bsSentiment(companyName):
    adapter = RedditAdapter()
    client = SocialClient(adapter)
    posts = client.get_posts(companyName, 20)

    sentiment = 0
    p = 0
    number_posts = len(posts)

    for i in range(10):
        sentiment_post = 0
        for post in posts:
            sentiment_post += sentiment_analysis_with_stochastic_model(post)    

        sentiment += sentiment_post/number_posts


    for post in posts:
        if get_post_sentiment(post) == 1:
            p += 1
            
    sentiment = sentiment * 1000 + (p / number_posts) * 100

    if sentiment >=0:
        return f"{sentiment:.2f}% positive"
    return f"{sentiment:.2f}% negative"



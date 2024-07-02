import sys
sys.path.append('./SentimentAnalysis')

from SocialClient import SocialClient, RedditAdapter, get_post_sentiment
from markov import get_sentiment_score

def markovSentiment(companyName):
    adapter = RedditAdapter()
    client = SocialClient(adapter)
    posts = client.get_posts(companyName, 40)
    score = 0

    for i in range(10):
        score += get_sentiment_score(posts)
    
    score = score * 100

    if score >=0:
        return f"{score:.2f}% positive"
    return f"{score:.2f}% negative"


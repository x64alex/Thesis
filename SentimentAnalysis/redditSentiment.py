import sys
sys.path.append('./SentimentAnalysis')

from SocialClient import SocialClient, RedditAdapter, get_post_sentiment

def redditSentiment(companyName):
    adapter = RedditAdapter()
    client = SocialClient(adapter)
    posts = client.get_posts(companyName, 20)

    positive = 0
    negative = 0
    number_posts = len(posts)

    for post in posts:
        sentiment = get_post_sentiment(post)
        if sentiment == 1:
            positive += 1
        elif sentiment == -1:
            negative += 1
            
    percentage_positive = round((positive / number_posts) * 100)
    percentage_negative = round((negative / number_posts) * 100)

    return f"{percentage_positive}% positive and {percentage_negative}% negative"



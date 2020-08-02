# ==============================
# FILE: GetTweets.py
# AUTH: Matt B. Jackson
# DATE: June 13th, 2020
# ==============================

# Import Required Libraries
import tweepy as tw
import pandas as pd

# Define Search Parameters
QUERY = "shopDisney -filter:retweets"
SINCE = "2020-06-14"
UNTIL = "2020-06-22"

# Initialize Twitter API
auth = tw.OAuthHandler("L5DuaenxIHeuHJXhEt88ezllI", "ot3Oy0yMK4yAjJFXMbQEzi0W7ik3BZmS5WU9gmtLhrUxYNLv58")
api = tw.API(auth, wait_on_rate_limit=True)

# Create Tweepy Cursor
tweets = tw.Cursor(api.search, q=QUERY, since=SINCE, until=UNTIL, lang="en").items(9999)

# Create Array of Tweet Data
data = [[tweet.created_at, tweet.text, tweet.user.screen_name, tweet.user.location] for tweet in tweets]

# Create Dataframe
data = pd.DataFrame(data=data, columns=["datetime", "text", 'user', "location"])

# Save Dataframe to CSV File
data.to_csv("../data/shopDisney.csv")

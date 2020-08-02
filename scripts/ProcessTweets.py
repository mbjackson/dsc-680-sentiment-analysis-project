# ==============================
# FILE: ProcessTweets.py
# AUTH: Matt B. Jackson
# DATE: June 13th, 2020
# ==============================

# Import Required Libraries
import pickle
import pandas as pd

# Load Tweets
tweets = pd.read_csv("../data/shopDisney.csv")

# Load Model
with open("../model.pkl", "rb") as file:
    pickle_model = pickle.load(file)

tweets["datetime"] = pd.to_datetime(tweets["datetime"])
tweets["date"] = tweets["datetime"].dt.date
tweets = tweets.drop(["Unnamed: 0", "datetime"], axis=1)
tweets = tweets.sort_values("date")

tweets["sentiment"] = pickle_model.predict(tweets.text)

# Save Dataframe to CSV File
tweets.to_csv("../data/shopDisney_Processed.csv")

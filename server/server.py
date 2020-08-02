import os
import pickle
import pandas as pd
from flask import Flask, render_template

app = Flask(__name__)


def evaluate():

    response = dict()

    with open("../model.pkl", "rb") as file:
        pickle_model = pickle.load(file)

    tweets = pd.read_csv("../data/shopDisney.csv", engine="python")
    tweets["datetime"] = pd.to_datetime(tweets["datetime"])
    tweets["date"] = tweets["datetime"].dt.date
    tweets = tweets.drop(["Unnamed: 0", "datetime"], axis=1)
    tweets = tweets.sort_values("date")
    tweets["sentiment"] = pickle_model.predict(tweets.text)

    response["range"] = str(tweets["date"].min()) + " through " + str(tweets["date"].max())
    response["average"] = round(tweets["sentiment"][tweets["sentiment"] == 4].count() / tweets[
            "sentiment"].count(), 2)
    response["totalTweets"] = len(tweets.index)
    response["totalPositiveTweets"] = tweets["sentiment"][tweets["sentiment"] == 4].count()
    response["totalNegativeTweets"] = tweets["sentiment"][tweets["sentiment"] == 0].count()

    response["dailyLabels"] = list()
    response["dailyValues"] = list()
    response["dailyValues2"] = list()

    for date in tweets.date.unique():
        tweets_filtered = tweets[tweets["date"] == date]
        positive = tweets_filtered["sentiment"][tweets_filtered["sentiment"] == 4].count() / tweets_filtered[
            "sentiment"].count()
        response["dailyLabels"].append(str(date))
        response["dailyValues"].append(round(positive, 2))
        response["dailyValues2"].append(round(1-positive, 2))

    return response


@app.route('/')
def index():
    response = evaluate()
    return render_template("index.html",
                           totalTweets=response["totalTweets"],
                           totalPositiveTweets=response["totalPositiveTweets"],
                           totalNegativeTweets=response["totalNegativeTweets"],
                           averageSentiment=response["average"],
                           range=response["range"],
                           dailyValues=response["dailyValues"],
                           dailyLabels=response["dailyLabels"],
                           dailyValues2=response["dailyValues2"])


os.system("python3 ../scripts/GetTweets.py")
app.run()

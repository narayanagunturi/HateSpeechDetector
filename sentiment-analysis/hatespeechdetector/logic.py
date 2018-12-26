import tweepy
import csv
import re
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline
import pickle
import numpy as np
import pandas as pd

def examine(query):
    gettweets(query)
    file1='Hate_Speech_detection_of_100_Tweets_About_'+query+'.csv'
    print(file1)
    values=train(file1)
    query=query.capitalize()
    pic=plot(values,query)
    print('testing done')
    print('test function')
    print(values)
    d={'Positive':values[0],'Negative':values[1],'result':pic}
    print(d)
    return values, pic

def authenticate():
    consumer_key = "enter your consumer key"
    consumer_secret = "enter your consumer secret"
    access_token = "enter your acces token"
    access_token_secret = "enter your acces token secret"

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api

def gettweets(query):
    query = query.lower()
    api = authenticate()
    number=100
    results = api.search(
   lang="en",
   q=query + " -rt",
   count=number,
   result_type="recent")
    print("--- Gathered Tweets \n")
    writetocsv(results, number, query) 

def writetocsv(results, number, query):
    file_name = 'Hate_Speech_detection_of_{}_Tweets_About_{}.csv'.format(number, query)
    with open(file_name, 'w') as csvfile:
        csv_writer = csv.DictWriter(
            f=csvfile,
            fieldnames=["Tweet", "Sentiment"])
        csv_writer.writeheader()
        print("--- Opened a CSV file to store the results of your sentiment analysis... \n")
        for c, result in enumerate(results, start=1):
            tweet = result.text
            tidy_tweet = tweet.strip()
            cleanedtweets = cleanTweets(tidy_tweet)
            if len(tweet) == 0:
                print('Empty Tweet')
                continue
            csv_writer.writerow({'Tweet': cleanedtweets})
            print("Analyzed Tweet {}".format(c))


def cleanTweets(raw_tweet):
    raw_tweet = remove_pattern(raw_tweet)
    raw_tweet = raw_tweet.lower()
    raw_tweet = raw_tweet.replace('\d+', '')
    return raw_tweet

def remove_pattern(input_txt):
    input_txt = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",str(input_txt)).split())
    return input_txt

def plot(values,user_input):
    print('in plot get')
    xs = range(1,3)
    ys = [values[0],values[1]]
    x = plt.bar(xs,ys)
    x[0].set_color('b')
    x[1].set_color('r')
    plt.xlabel('Sentiment')
    plt.ylabel('Percentage')
    yaxis=['Positive','Negative']
    plt.xticks(xs,yaxis)
    plt.savefig('E:/bar.png')
    plt.title('Hate Speech Detection for %s'% user_input)
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue()).decode('ascii')
    result = figdata_png
    print('generated result')
    print(result)
    return result

def train(filename):
    print('created classifier')
    f = open('E:/pipeline.pickle', 'rb')
    classifier = pickle.load(f)
    print('opened classifier')
    print('in test data function')
    test_data = pd.read_csv(filename)
    clean_test_tweets = []
    data_set_length=len(test_data)
    for i in range(0,data_set_length):
        if((i+1)%10==0):
            print ('Tweet of  %d of %d\n'%(i+1,data_set_length))
        clean_tweets = cleanTweets(test_data['Tweet'][i])
        clean_test_tweets.append(clean_tweets)
    print(clean_test_tweets)
    print('after reading')
    result = classifier.predict(clean_test_tweets)
    f.close()
    print(result)
    test_data['Sentiment']= result
    test_data.to_csv(filename)
    lentest = len(test_data)
    pos = len(test_data[test_data['Sentiment']=='0'])
    neg = len(test_data[test_data['Sentiment']=='1'])
    pos_percent = round((pos*100)/lentest, 2)
    neg_percent = round((neg*100)/lentest, 2)
    print('positive percentage is: %d' %pos_percent)
    print('negative percentage is: %d' %neg_percent)
    l=[]
    l=[pos_percent,neg_percent]
    return l
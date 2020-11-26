import re

import fasttext
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
from bs4 import BeautifulSoup
import re
import itertools
import emoji
import geocoder


# emoticons
def load_dict_sadsmileys():
    return {
        ":‑(": "sad",
        ":‑c": "sad",
        ":‑<": "sad",
        ":‑[": "sad",
        ":(": "sad",
        ":c": "sad",
        ":<": "sad",
        ":[": "sad",
        ":-||": "sad",
        ">:[": "sad",
        ":{": "sad",
        ":@": "sad",
        ">:(": "sad",
        ":'‑(": "sad",
        ":'(": "sad"
    }


def load_dict_smileys():
    return {
        ":‑)": "smiley",
        ":-]": "smiley",
        ":-3": "smiley",
        ":->": "smiley",
        "8-)": "smiley",
        ":-}": "smiley",
        ":)": "smiley",
        ":]": "smiley",
        ":3": "smiley",
        ":>": "smiley",
        "8)": "smiley",
        ":}": "smiley",
        ":o)": "smiley",
        ":c)": "smiley",
        ":^)": "smiley",
        "=]": "smiley",
        "=)": "smiley",
        ":-))": "smiley",
        ":‑D": "smiley",
        "8‑D": "smiley",
        "x‑D": "smiley",
        "X‑D": "smiley",
        ":D": "smiley",
        "8D": "smiley",
        "xD": "smiley",
        "XD": "smiley",
        ":‑P": "playful",
        "X‑P": "playful",
        "x‑p": "playful",
        ":‑p": "playful",
        ":‑Þ": "playful",
        ":‑þ": "playful",
        ":‑b": "playful",
        ":P": "playful",
        "XP": "playful",
        "xp": "playful",
        ":p": "playful",
        ":Þ": "playful",
        ":þ": "playful",
        ":b": "playful",
        "<3": "love"
    }


# self defined contractions
def load_dict_contractions():
    return {
        "ain't": "is not",
        "amn't": "am not",
        "aren't": "are not",
        "can't": "cannot",
        "'cause": "because",
        "couldn't": "could not",
        "couldn't've": "could not have",
        "could've": "could have",
        "daren't": "dare not",
        "daresn't": "dare not",
        "dasn't": "dare not",
        "didn't": "did not",
        "doesn't": "does not",
        "don't": "do not",
        "e'er": "ever",
        "em": "them",
        "everyone's": "everyone is",
        "finna": "fixing to",
        "gimme": "give me",
        "gonna": "going to",
        "gon't": "go not",
        "gotta": "got to",
        "hadn't": "had not",
        "hasn't": "has not",
        "haven't": "have not",
        "he'd": "he would",
        "he'll": "he will",
        "he's": "he is",
        "he've": "he have",
        "how'd": "how would",
        "how'll": "how will",
        "how're": "how are",
        "how's": "how is",
        "I'd": "I would",
        "I'll": "I will",
        "I'm": "I am",
        "I'm'a": "I am about to",
        "I'm'o": "I am going to",
        "isn't": "is not",
        "it'd": "it would",
        "it'll": "it will",
        "it's": "it is",
        "I've": "I have",
        "kinda": "kind of",
        "let's": "let us",
        "mayn't": "may not",
        "may've": "may have",
        "mightn't": "might not",
        "might've": "might have",
        "mustn't": "must not",
        "mustn't've": "must not have",
        "must've": "must have",
        "needn't": "need not",
        "ne'er": "never",
        "o'": "of",
        "o'er": "over",
        "ol'": "old",
        "oughtn't": "ought not",
        "shalln't": "shall not",
        "shan't": "shall not",
        "she'd": "she would",
        "she'll": "she will",
        "she's": "she is",
        "shouldn't": "should not",
        "shouldn't've": "should not have",
        "should've": "should have",
        "somebody's": "somebody is",
        "someone's": "someone is",
        "something's": "something is",
        "that'd": "that would",
        "that'll": "that will",
        "that're": "that are",
        "that's": "that is",
        "there'd": "there would",
        "there'll": "there will",
        "there're": "there are",
        "there's": "there is",
        "these're": "these are",
        "they'd": "they would",
        "they'll": "they will",
        "they're": "they are",
        "they've": "they have",
        "this's": "this is",
        "those're": "those are",
        "'tis": "it is",
        "'twas": "it was",
        "wanna": "want to",
        "wasn't": "was not",
        "we'd": "we would",
        "we'd've": "we would have",
        "we'll": "we will",
        "we're": "we are",
        "weren't": "were not",
        "we've": "we have",
        "what'd": "what did",
        "what'll": "what will",
        "what're": "what are",
        "what's": "what is",
        "what've": "what have",
        "when's": "when is",
        "where'd": "where did",
        "where're": "where are",
        "where's": "where is",
        "where've": "where have",
        "which's": "which is",
        "who'd": "who would",
        "who'd've": "who would have",
        "who'll": "who will",
        "who're": "who are",
        "who's": "who is",
        "who've": "who have",
        "why'd": "why did",
        "why're": "why are",
        "why's": "why is",
        "won't": "will not",
        "wouldn't": "would not",
        "would've": "would have",
        "y'all": "you all",
        "you'd": "you would",
        "you'll": "you will",
        "you're": "you are",
        "you've": "you have",
        "Whatcha": "What are you",
        "luv": "love",
        "sux": "sucks"
    }


class TwitterClient(object):
    '''
	Generic Twitter Class for sentiment analysis.
	'''

    def __init__(self):
        '''
		Class constructor or initialization method.
		'''
        # keys and tokens from the Twitter Dev Console
        consumer_key = 'm6Q1IHRfFdjuIGorHeQB78EJS'
        consumer_secret = 'MXGFHXQOafroNydd33LS7JnGI0YKqjboodjGwLftKsMMJ3QX4r'
        access_token = '1328743781466828805-32v0JhuKObxxFqCN2cpMrjOqnBJdbB'
        access_token_secret = 'oebvQBbijNsZedXEuCFew9xVbc4zff1GcjTallpjMlaav'

        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")

    def clean_tweet(self, tweet):
        '''
		Utility function to clean tweet text by removing links, special characters
		using simple regex statements.
		'''
        # Escaping HTML characters
        tweet = BeautifulSoup(tweet).get_text()

        # Special case not handled previously.
        tweet = tweet.replace('\x92', "'")

        # Removal of hastags/account
        tweet = ' '.join(re.sub("(@[A-Za-z0-9]+)|(#[A-Za-z0-9]+)", " ", tweet).split())

        # Removal of address
        tweet = ' '.join(re.sub("(\w+:\/\/\S+)", " ", tweet).split())

        # Removal of Punctuation
        tweet = ' '.join(re.sub("[\.\,\!\?\:\;\-\=]", " ", tweet).split())

        # Lower case
        tweet = tweet.lower()

        # CONTRACTIONS source: https://en.wikipedia.org/wiki/Contraction_%28grammar%29
        CONTRACTIONS = load_dict_contractions()
        tweet = tweet.replace("’", "'")
        words = tweet.split()
        reformed = [CONTRACTIONS[word] if word in CONTRACTIONS else word for word in words]
        tweet = " ".join(reformed)

        # Standardizing words
        tweet = ''.join(''.join(s)[:2] for _, s in itertools.groupby(tweet))

        # Deal with emoticons source: https://en.wikipedia.org/wiki/List_of_emoticons
        SMILEY = load_dict_smileys()
        words = tweet.split()
        reformed = [SMILEY[word] if word in SMILEY else word for word in words]
        tweet = " ".join(reformed)

        SADSMILEY = load_dict_sadsmileys()
        words = tweet.split()
        reformed = [SADSMILEY[word] if word in SADSMILEY else word for word in words]
        tweet = " ".join(reformed)

        # Deal with emojis
        tweet = emoji.demojize(tweet)

        tweet = tweet.replace(":", " ")
        tweet = ' '.join(tweet.split())

        return tweet

    def get_tweet_sentiment(self, tweet):
        '''
		Utility function to classify sentiment of passed tweet
		using textblob's sentiment method
		'''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def get_tweets(self, query, count=500000):
        '''
		Main function to fetch tweets and parse them.
		'''
        # empty list to store parsed tweets
        tweets = []

        try:
            # call twitter api to fetch tweets
            fetched_tweets = self.api.search(q=query, count=count)

            # parsing tweets one by one
            for tweet in fetched_tweets:
                # empty dictionary to store required params of a tweet

                # print(tweet)

                parsed_tweet = {}

                # saving text of tweet
                parsed_tweet['text'] = tweet.text

                parsed_tweet['uid'] = tweet.user.id

                parsed_tweet['date'] = tweet.created_at

                parsed_tweet['username'] = tweet.user.name

                parsed_tweet['userscreenname'] = tweet.user.screen_name

                result = geocoder.arcgis(tweet.place)

                parsed_tweet['tweetlocation'] = (result.x, result.y)

                # saving sentiment of tweet
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

                parsed_tweet['retweet_count'] = tweet.retweet_count

                parsed_tweet['favorite_count'] = tweet.favorite_count

                parsed_tweet['favorite_count'] = tweet.favorite_count

                parsed_tweet['tac'] = tweet.retweet_count + tweet.favorite_count

                # appending parsed tweet to tweets list
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)

            # return parsed tweets
            return tweets

        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))


def get_topics_basedon_tac(topicCommentDict):
    newDict = {}
    for key, value in sorted(topicCommentDict.items(), key=lambda r: r[1][2], reverse=True):
        newDict[key] = value
    return newDict


def controvercy_rate(topicsbasedontac):
    contovercial_topics_list = []

    for topic in topicsbasedontac:
        topic_obj = {}
        list, total_negative_tweets, total_neg_pos_tweets, tac = topicsbasedontac[topic]
        cr = (total_negative_tweets / total_neg_pos_tweets) * 100
        if (cr >= 40):
            topic_obj["topic"] = topic
            topic_obj["cr"] = cr
            topic_obj["remark"] = "controversial"
            topic_obj["tweetanduserdatalist"] = list
            contovercial_topics_list.append(topic_obj)

    return contovercial_topics_list


def main():
    # creating object of TwitterClient Class
    api = TwitterClient()
    # calling function to get tweets
    listOfTopics = ['Election', 'Trump', 'Gray is the new black', 'The rise of the robots', 'joe biden', 'terrorism',
                    'AI']
    topicCommentDict = {}
    for topic in listOfTopics:
        taccount = 0
        tweets = api.get_tweets(query=topic, count=5000000)

        # picking positive tweets from tweets
        ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']

        for ptweet in ptweets:
            taccount = taccount + ptweet['tac']

        # percentage of positive tweets
        # print("Positive tweets percentage: {} %".format(100 * len(ptweets) / len(tweets)))
        # picking negative tweets from tweets
        ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']

        for ntweet in ntweets:
            taccount = taccount + ntweet['tac']
        # percentage of negative tweets

        taccount += len(ptweets) + len(ntweets)

        topicCommentDict[topic] = ({'list': ntweets}, len(ntweets), len(ntweets) + len(ptweets), taccount)


    topicsbasedontac = get_topics_basedon_tac(topicCommentDict)
    topicobj = controvercy_rate(topicsbasedontac)
    print(topicobj)


if __name__ == "__main__":
    # calling main function
    main()

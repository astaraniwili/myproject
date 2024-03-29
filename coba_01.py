# -*- coding: utf-8 -*-
"""coba_01.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1QUi4Yq7zeFKq5V6XadQZALRdKwtlQOoM

#Bussiness Understanding

Kali ini akan menganalisis sentimen untuk data teks dari twitter dan data dari portal berita kompas.com. Topik yang diambil kali ini adalah ktt g20

#Data Understanding
"""

# pip install tweepy==4.10.1

pip install streamlit

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import tweepy
import requests
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import LancasterStemmer
from nltk.probability import FreqDist
import seaborn as sns
from bs4 import BeautifulSoup

"""##Twitter"""

with open("token_mytwit2.json")as f:
  tokens = json.load(f)

bearer_token = tokens['bearer_token']
api_key = tokens['api_key']
api_key_secret = tokens['api_key_secret']
access_token = tokens['access_token']
access_token_secret = tokens['access_token_secret']

import tweepy

api = tweepy.Client(bearer_token=bearer_token, wait_on_rate_limit=True)

query = "ktt g20 -is:retweet lang:id"

response = tweepy.Paginator(api.search_recent_tweets,
                          query = query,
                          max_results=100
                          ).flatten(limit=1001)

tweets = [tweet.text.strip() for tweet in response]
df_tweets = pd.DataFrame(tweets, columns=["tweets"])
# st.dataframe(df_tweets, use_container_width=True)

df_tweets

st.dataframe(df_tweets, use_container_width=True)

from pandas.core.reshape.merge import string
def case_folding(data):
    data = data.lower()
    data = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",data).split())
    data = re.sub(r"\d+", "", data)
    data = data.translate(str.maketrans("","",string.punctuation))
    data = re.sub(r"\n","",data)
    data = re.sub(r"\t","",data)
    return data
df_tweets['tweet_clean'] = df_tweets['tweets'].apply(case_folding)
df_tweets

st.dataframe(df_tweets, use_container_width=True)

nltk.download('stopwords')
from nltk.corpus import stopwords
stop_words = stopwords.words('indonesian')

def clean_stopwords(text):
  word_list = text.split()
  text = ' '.join(i for i in word_list if i not in stop_words)
  return text

df_tweets['tweet_clean'] = df_tweets['tweet_clean'].apply(clean_stopwords)
df_tweets

st.dataframe(df_tweets, use_container_width=True)

pip install PySastrawi

nltk.download('punkt')
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
factory = StemmerFactory()
stemmer = factory.create_stemmer()
def stemSentence(sentence):
    token_words=word_tokenize(sentence)
    token_words
    stem_sentence=[]
    for word in token_words:
        stem_sentence.append(stemmer.stem(word))
        stem_sentence.append(" ")
    return "".join(stem_sentence)

df_tweets['tweet_clean'] = df_tweets['tweet_clean'].apply(stemSentence)
df_tweets

st.dataframe(df_tweets, use_container_width=True)

with open("./kata_positif.txt","r") as positif_file :
  positive_words = list(set(positif_file.readlines()))
with open("./kata_negatif.txt","r") as negative_file :
  negative_words = list(set(negative_file.readlines()))

hasil = []
list_negasi = ['tidak','lawan','anti', 'tdk', 'jangan', 'gak', 'enggak', 'bukan', 'tak']

for tweet in tweets:

    tweet_clean = tweet.strip().split()
    
    good_count = 0 #nilai positif
    bad_count = 0 #nilai negatif

    for good_word in positive_words:
        count = tweet_clean.count(good_word.strip().lower())
        if count > 0:
          print(good_word.strip())
          good_count += count

    for bad_word in negative_words:
        count = tweet_clean.count(bad_word.strip().lower())
        if count > 0:
          print(bad_word.strip())
          bad_count += count
    
    print ("positif: "+str(good_count))
    print ("negatif: "+str(bad_count))
    hasil.append(good_count - bad_count)
    print ("-----------------------------------------------------")

sentiments = ["positif" if sentimen > 0 else ("netral" if sentimen == 0 else "negatif") for sentimen in hasil]
df_tweets["sentiment"] = sentiments
df_tweets

st.dataframe(df_tweets, use_container_width=True)

print (f'''
Mean: {np.mean(hasil)}
Median: {np.median(hasil)}
quartil awal: {np.quantile(hasil,0.25)}
quartil akhir: {np.quantile(hasil,0.75)}
Standar deviasi: {np.std(hasil)}     
''')

labels, counts = np.unique(hasil, return_counts=True)

fig, ax = plt.subplots()
ax.set_xticks(ax.get_xticks())
ax.figure.savefig('file.png')
sns.barplot(x = list(labels), 
            y = list(counts))

sns.lineplot(x = ax.get_xticks(), 
            y = list(counts))

plt.title(f'Distribution Sentiment')
plt.xlabel('Labels')
plt.ylabel('Counts')

plt.show()

st.pyplot(fig)

sns.barplot(df_tweets['sentiment'].value_counts().index,df_tweets['sentiment'].value_counts())
ax.figure.savefig('file2.png')
plt.show()

st.pyplot(fig)

"""##Website"""

kompas = requests.get('https://www.kompas.com/')
kompas.content

beautify = BeautifulSoup(kompas.content)
beautify

populer = beautify.find('div',{'class','most__wrap clearfix'})
populer

berita = populer.find_all('div',{'class','most__list clearfix'})
berita

for each in berita:
  nomor = each.find('div',{'class','most__count'}).text
  judul = each.find('h4',{'class','most__title'}).text
  link = each.a.get('href')
  print(nomor)
  print(judul)
  print(link)
  print('')

berita_populer=[]

for i in range(1, 10):
    URL = "https://www.kompas.com/"
    kompas = requests.get(URL)
    
    soup = BeautifulSoup(kompas.content, 'html5lib') # If this line causes an error, run 'pip install html5lib' or install html5lib
   
    populer = soup.find('div',{'class','most__wrap clearfix'})
    berita = populer.find_all('div',{'class','most__list clearfix'})
    
    for each in berita:
        list_berita = {}
        list_berita['nomor'] = each.find('div',{'class','most__count'}).text
        list_berita['judul berita populer'] = each.find('h4',{'class','most__title'}).text
        list_berita['link'] = each.a.get('href')
        berita_populer.append(list_berita)

pd.DataFrame(berita_populer)

st.dataframe(berita_populer)

# import requests
# from bs4 import BeautifulSoup

# page = 1

# berita=[]  # a list to store quotes

# for i in range(1, 10):
#     URL = "https://search.kompas.com/search/?q=ktt+g20&submit=Kirim#gsc.tab=0&gsc.q=ktt%20g20&gsc.page={}".format(page)
#     r = requests.get(URL)
    
#     soup = BeautifulSoup(r.content, 'html5lib') # If this line causes an error, run 'pip install html5lib' or install html5lib
   
#     table = soup.find('div', attrs = {'id': 'ktt g20'})
    
#     for row in table.findAll('div',
#                             attrs = {'class':'col-6 col-lg-4 text-center margin-30px-bottom sm-margin-30px-top'}):
#         quote = {}
#         quote['theme'] = row.h5.text
#         quote['url'] = row.a['href']
#         quote['img'] = row.img['src']
#         quote['lines'] = row.img['alt'].split(" #")[0]
#         quote['author'] = row.img['alt'].split(" #")[1]
#         berita.append(quote)

#     page = page + 1

# kompas_berita = requests.get('https://search.kompas.com/search/?q=ktt+g20&submit=Kirim#gsc.tab=0&gsc.q=ktt%20g20&gsc.page={}')
# kompas_berita.content

# beautify_berita = BeautifulSoup(kompas_berita.content)
# # beautify_berita


import snscrape.modules.twitter as sntwitter
import pandas as pd
import streamlit as st
from streamlit_lottie import st_lottie
import requests
import pymongo
import datetime

st.set_page_config(page_title='Twitter Scrapping', page_icon=':hash:', layout='wide')

#Animations 
def load_lottieur(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()  
lottie_coding = load_lottieur("https://assets7.lottiefiles.com/packages/lf20_5mhyg2hz.json")  

#title 
with st.container():
    left_column,right_column = st.columns(2)
    with left_column:
        st.title("Twitter Scrapping :hash:")
    with right_column:
        st_lottie(lottie_coding,height=150, key='codings')

#keyword or hastag to be entered        
keyword = st.text_input('What do you want to search for?',)

#Date
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Start Date",datetime.date(2022, 11, 11))
    st.write('start date is:',start_date)

with col2:
    stop_date = st.date_input("Stop Date",datetime.date(2022, 12, 30))
    st.write('Stop date:', stop_date)

# Converting the datatype to String
from_date = str(start_date)
until_date = str(stop_date)

#slider to adjust the size of tweets
max_tweets = st.slider('Select the number of tweets to be displayed : ',10, 1000)

#list to append the tweets
tweets = []

def tweets_scrap():
#TwitterSearchScraper function of snscrape to scrape data and append it tweets to list
	for i, tweet in enumerate(
			sntwitter.TwitterSearchScraper(f'{keyword} since:{from_date} until:{until_date}').get_items()):
    
		if i > max_tweets:
			break
		tweets.append([tweet.date, tweet.id, tweet.url, tweet.content, tweet.user.username,
					   tweet.likeCount])

	#Creating a dataframe
	tweets_df = pd.DataFrame(tweets, columns=['Datetime', 'Tweet Id', 'URL', 'Content', 'Username','LikesCount'])

	#Displaying dataframe 
	st.dataframe(tweets_df)

	#Creating a download button to download csv file
	st.download_button('Download CSV',
					   tweets_df.to_csv(),
					   file_name='Twitter_Data.csv',  
					   mime='text/csv')

if st.button("Show Tweets"):
	if keyword:
		tweets_scrap()

#if st.button('Upload To Database'):
                # Making a Connection with MongoClient
                
                #client = MongoClient(("mongodb://localhost:27017"))
               

                # database
                #db = client["Tweet_Scrap"]
                #db = client.Twitter_Scrap

                # collection
                #tweet_db = db["Hash_detail"]
                #tweet_db = db.Hash_detail

                #Converts dataframe into dictonary 
                #data_dict = tweets_df.to_dict("records")

                # Insert collection
                #tweet_db.insert_many(data_dict)
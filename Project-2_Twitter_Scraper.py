# First, Importing all the Necessary Library packages..
import streamlit as st                                      # Importing Streamlit to create GUI to get the Input from USER.
import pandas as pd                                         # To convert List of Datas into Dataframe.. (Table format)
import snscrape.modules.twitter as sntwitter                # To Scrape the Tweets from Twitter..
from datetime import datetime                               # To convert into datetime format..
import pymongo                                              # To import the Scraped Tweets into the Mongo Database..

# To create Front interface for USER using Streamlit:
st.set_page_config(page_title='TWITTER SCRAPER')   # Browser Streamlit Tab name..
st.header('Twitter Data Scraper')  # Header in Streamlit page..
st.markdown('_Enter the KEYWORD, DATE and TWEET LIMITS to scrape_')   # Text informations to USER..


# Creating input space to USER (For getting Keyword, No. of Tweets to be sraped):
col1,col2=st.columns(2)
with col1:
    Key_Word=st.text_input('Enter KEYWORD: ')
with col2:
    Tweet_limit=st.text_input('Enter TWEET limit: ')

# Creating input space to USER (For getting Start and End date to scrape Tweets):
col3,col4=st.columns(2)
with col3:
    Since_date=st.date_input('Enter START date: ')
with col4:
    Until_date=st.date_input('Enter END date: ')

# Def a variable to Concatenate the Keyword with Date limits:
Query_with_date=Key_Word+' '+'until:'+str(Until_date)+' '+'since:'+str(Since_date)


# In order to avoid reloading of page after 'Submit' button clicked, Session_State used.. (To stay in True Position)..
if 'Submit_button_clicked' not in st.session_state:
    st.session_state.Submit_button_clicked=False

# Fn called to change Session_State condition..
def callback():
    st.session_state.Submit_button_clicked=True

# If 'Submit' button clicked, Session_State will become True..
if (st.button('Submit', on_click=callback) or st.session_state.Submit_button_clicked):

    if len(Key_Word)!=0:                                                      # Checking Lenght of the Keyword..
        if len(Tweet_limit)!=0 and Tweet_limit!='0':                          # Checking Lenght of the Tweet Limit and Its value should not be 0..
            st.write('Thanks for Reaching.. Your Data is here..')
            Tweet_Storage=[]

            # Scrapping the Tweets from Twitter, using SNTWITTER and Storing them in Tweet_Storage..
            for Tweet in sntwitter.TwitterSearchScraper(Query_with_date).get_items():
                if len(Tweet_Storage)<int(Tweet_limit):
                    Tweet_Storage.append([Tweet.date,Tweet.id,Tweet.url,Tweet.user,Tweet.content,Tweet.replyCount,Tweet.retweetCount,Tweet.likeCount,Tweet.lang,Tweet.source])
                else:
                    break

            if len(Tweet_Storage)!=0:             # Checking No. of Tweets in Tweet_Storage.. If its equal to 0, It show a caption..

                # Converting Data's in Tweet_Storage into DataFrame:
                df=pd.DataFrame(Tweet_Storage, columns=['Date','ID','URL','User','Content','Reply Count','ReTweet Count','Like Count','Language','Source'])
                Data_Frame_View=st.dataframe(df)

                # Creating Buttons to Download CSV, Download json, Importing to Mongo Database:
                Download_csv=st.download_button("Download CSV",df.to_csv(),file_name='Twitter_data.csv',mime='text/csv')                    # Converting Dataframe to CSV format
                Download_json=st.download_button('Download json', df.to_json(), file_name='Twitter_data.json', mime='application/json')     # Converting Dataframe to json format


                Import_to_DB=st.button('Import to MongoDB')
                if Import_to_DB:                                                        # If Import to DB is Clicked, It connects with pymongo Client..
                    client = pymongo.MongoClient("mongodb://localhost:27017/")
                    mydb = client["Twitter_DB"]                                         # Creating Database
                    mycol = mydb["Twitter_Scraped_Data"]                                # Creating Collection
                    time_stamp = datetime.timestamp(datetime.now())                     # Creating Time_stamp for current datetime..
                    Key_ID = Key_Word + str(time_stamp)                                 # Creating Key_ID by combining Keyword + timestamp (To create unique id for every scraping..)
                                                                                        # Eg:({“Keyword+current Timestamp”: [{1000 Scraped data from past 100 days }]})
                    df_dict_format=df.to_json()                                         # Converting Dataframe to Dict format
                    insert_DB = mycol.insert_one({Key_ID:[df_dict_format]})             # Inserting the scraped Tweets as a document in the collection..
                    st.write('Successfully Imported in DataBase..')

            # If NO Tweets found for given details, It shows a caption, to change the details (Keyword & Date) and Try again.. At the same time, it changed the Session_State condition to False..
            else:
                st.caption('Sorry.. No Tweet for the given details.. Please try again with different Keyword or Date limit or Tweet limit..')
                st.session_state.Submit_button_clicked=False

        # It shows an Error, If Tweet limit column is empty or providing '0' value.. At the same time, it changed the Session_State condition to False..
        else:
            st.error('Atleast 1 data need to scrape.. Please enter valid No. of Tweets to Scrape..')
            st.session_state.Submit_button_clicked=False

    # It shows an Error, if Keyword column is empty.. At the same time, it changed the Session_State condition to False..
    else:
        st.error('Keyword is Mandatory.. Please enter...')
        st.session_state.Submit_button_clicked=False


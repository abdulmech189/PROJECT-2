# PROJECT-2
TWITTER Data Scraping

Problem: To scrape the data like (date, id, url, tweet content, user,reply count, retweet count,language, source, like count etc) from TWITTER based on Keyword, Time period given by the user..

Imported Libraries:
1. Streamlit - To create a Front end user interface to get the input..
2. snscrape - It is specially used to scrape datas from Social media platform, like Facebook, Twitter etc..
3. pymongo - To export scraped datas into Mongo Database.. pymongo connects python IDE with MongoDB server..
4. pandas - To convert scraped datas in Dataframe format (Table format)
5. datetime - To handle with datetime objects..

Step 1: Creating GUI interface using Streamlit:
Created the Streamlit tab name, Header, Text informations in the interface..
To collect the Input from the user, 4 Columns created (Keyword, Tweet limit, Start date, End date)..
St.Session_State used to stay 'Submit' button in True state, if any other button we click.. It will avoid reloading of page again and again..

Step 2: Scraping Tweets from Twitter:
Using FOR loop, Data scraped and stored in a variable 'Tweet'.. 
After checking with the Tweet limit range, it is the appended into the Temporary list 'Tweet_Storage'..
It will scrape the Tweets until Tweet limit given by the user..

Step 3: Converting the scraped datas into Dataframe:
Converting the Tweets which is stored in Temporary list in Dataframe using Pandas..
It is also viewed in Streamlit interface...

Step 4: Creating 3 buttons for USER:
1. Download CSV: Here, St.Download button created and the Dataframe file is converted into required CSV format..
2. Download json: Similary, another Download button created to download the file in json format. Here, Dataframe file is converted into json format..
3. Import to DB: Another button created to import the Scraped data into the Mongo Database.. When this button is clicked, python will connect with MongoDB server, Then it will call particular Database, collection and will store the Scraped data with Key_ID of each Scraping.. (Key_ID is created with Keyword searching and Current Timestamp..)


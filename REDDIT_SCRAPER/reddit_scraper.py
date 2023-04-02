import pandas as pd
from datetime import timedelta, datetime
import time
import praw
import re
import requests
import json
from psaw import PushshiftAPI

class Scraper(object):
    def __init__(self, date):
        self.date=date

    def get_comments(self):
        datefordf=self.date.strftime('%m-%d-%Y')
        dateforfilename=self.date.strftime('%Y-%m-%d')
        datetocheck=self.date.strftime('%B %d, %Y')
        
        thread = "Daily Discussion Thread for " + str(datetocheck)
        
        reddit = praw.Reddit(
            user_agent="Comment Extraction (by u/ilawmillig)",
            client_id="MIPcUKdUt2J1aw",
            client_secret="3do5ig4JfoOH1cacO5FOhl5JurSVxw",
            username="ilawmillig",
            password="Reddevils0@"
        )

        for submission in reddit.subreddit('wallstreetbets').search(thread):
            if submission.title==thread:
                link=submission.permalink
                id=submission.id
                url="https://www.reddit.com"+str(link)
                break    
            
        try:
            api=PushshiftAPI()
            comments=api.search_comments(subreddit={"wallstreetbets"}, link_id=id)
            total=0
            totalcomments=[]
            for comment in comments:
                body=comment.body
                text=body.split()
                totalcomments=totalcomments+text
                total=total+1            
        
            filename="STOCK_LIST04_25_2021.csv"
            df=pd.read_csv("/Users/milligil/Desktop/OTHER_EDUCATION/PYTHON_PROJECT/REDDIT_SCRAPER/STOCK_LISTS/"+filename)
            total_stock_list=df.Stock.tolist()

            stock_list=[]
            for word in totalcomments:
                word=re.sub('[^\w]','',word)
                word.replace("'s","")
                if word.upper() in total_stock_list:
                    stock_list.append(word.upper())
                else:
                    pass

            #Getting NOT_STOCKS list
            filename="NOT_STOCKS.csv"
            df=pd.read_csv("/Users/milligil/Desktop/OTHER_EDUCATION/PYTHON_PROJECT/REDDIT_SCRAPER/"+filename)
            not_stocks=df.SYMBOL.tolist()

            #Deleting entries found in NOT_STOCKS list
            new_stock_list=[]
            for word in stock_list:
                if word in not_stocks:
                    pass
                else:
                    new_stock_list.append(word.upper())

            #Getting file of common english words
            filename="COMMON_ENGLISH_WORDS"+".csv"
            df=pd.read_csv("/Users/milligil/Desktop/OTHER_EDUCATION/PYTHON_PROJECT/REDDIT_SCRAPER/"+filename)
            common_words=df.Word.tolist()

            #removing common words
            final_stock_list=[]
            for entry in new_stock_list:
                if entry.lower() in common_words:
                    pass
                else:
                    final_stock_list.append(entry.upper())

            #Counting mentions of stock, putting them in duplicate_list
            mentions={i:final_stock_list.count(i) for i in final_stock_list}
            
            mentions_df=[]
            for i in mentions:
                d={}
                d["Symbol"]=i
                d["Mentions"]=mentions[i]
                mentions_df.append(d)
            
            mentions_df=pd.DataFrame(mentions_df).sort_values(by="Mentions", ascending=False)
            mentions_df=mentions_df[mentions_df["Mentions"]>2]
            mentions_df.reset_index(inplace=True)
            del mentions_df["index"]
            
            mentions_df['Total Comments']=''
            mentions_df['Total Comments'][0]=total
            mentions_df['Date']=''
            mentions_df['Date'][0]=datefordf
            
            filename=dateforfilename+".csv"
            mentions_df.to_csv("/Users/milligil/Desktop/STOCK_DATABASE/REDDIT_MENTIONS/SCRAPES/"+filename, index=False)
            
            print(mentions_df)
            return mentions_df
        
        except:
            print(datefordf + " did not work!")

if __name__ == '__main__':
    testdate=datetime(2022,5,9)
    s=Scraper(testdate)
    s.get_comments()        






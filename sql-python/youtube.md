# Introduction


![image](https://user-images.githubusercontent.com/53164959/73610919-e77ed180-461f-11ea-8569-2879b34a7ba9.png)

Youtube is one of the biggest media intermediaries around the world. Thanks to its popularity, Korean entertainment has enjoyed 
the unprecedented level of popularity in its history from almost every continent in this universal. 
Its fame comes from Korean Pop so-called K-pop. This Asian culture  has wholly engrossed many western countries into this industry. 
To see the influence of this 'culture invasion on the U.S.A, I decided to collect some data from youtube API.  
This lengthy code is all about a series of searching, collecting, and storing the data into a table. 



![image](https://user-images.githubusercontent.com/53164959/73610971-6d028180-4620-11ea-847f-bae6a23304a4.png)

```python
import psycopg2 as ppg2
import json
import os
import sys
import time
from apiclient.discovery import build
from apiclient.errors import HttpError
from datetime import datetime,timedelta
import re
import logging
import pandas as pd


def main():
    api_key='replace_me'
    try:
        conn_string = "host='replace_me' dbname ='replace_me' user='replace_me' password=replace_me port=5432"
        conn = ppg2.connect(conn_string)
        cursor=conn.cursor()
    except:
        logging.error('can not acces the db')
        sys.exit(1)

    youtube_search_keyword(cursor=cursor,api_key=api_key,query='kpop',maxResults=50,regionCode='us',start_time='1912-01-01',time_interval='23 days')
    cursor.execute("SELECT * FROM youtube;")
    result=cursor.fetchall()
    your_dateframe=pd.DataFrame(result)
    print(your_dateframe) 



class DateTypeError(Exception):
    pass

'''
Normally, search is made on daily or weekly baiss. Thererfore, the value should contain specific number followed by either 'days' or 'weeks'
No monthly or yearly basis is not permitted for convenience. The value must be string , neither integer nor date type.
'''
def youtube_search_keyword(cursor,api_key,query,start_time,time_interval,maxResults=5,regionCode=None):

    if type(start_time)!=str and type(time_interval)!=str:
        raise DateTypeError
    else:
        timeRecord=date_conversion(date=start_time,time_interval=time_interval)
        start_time=timeRecord[0]
        end_time=timeRecord[1]
    try:
        youtube_object=build('youtube','v3',developerKey=api_key)
        search_key_word=youtube_object.search().list(q=query,part='snippet',maxResults=maxResults,regionCode=regionCode,publishedAfter=start_time,publishedBefore=end_time).execute()
        for index in search_key_word['items']:
            #search_key_word['items'][i] each dict contains the numerous keys and following values,one of which
            #we are interested in is 'snippet'. The keys are publishedAt,channelId,title,description,channelTitle,liveBroadcastContent
            default=index['snippet']['thumbnails']['default']['url']
            if default!='none':
                url=default
            else:
                url=None
            data={'channelid':index['snippet']['channelId'],
                  'publishedat':index['snippet']['publishedAt'],
                  'title':index['snippet']['title'],
                  'description':index['snippet']['description'],
                  'url':index['snippet']['thumbnails']['default']['url'],
                  'channeltitle':index['snippet']['channelTitle']
                  }
            
            #If your table contains primary key,implement the function called insert_valus_primary.
            insert_values(cursor,data,'youtube')

    except HttpError as e: #e.resp.status/e.content
      error_code=e.resp.status
      e=json.loads(e.content)
      error_msg=e['error']['errors'][0]['reason']
      print("Error_code : %s \nError Message : %s" %(error_code,error_msg))


def date_conversion(date,time_interval):
    date=date.split('-')
    date=list(map(int,date))
    start_date=datetime(year=date[0],month=date[1],day=date[2])
    if time_interval.find('weeks'):
        weeks=int(re.match('[1-5]+',time_interval).group())
        end_date=start_date+timedelta(weeks=weeks)
    elif time_interval.find('days'):
        days=int(re.match('[1-9]+',time_interval).group())
        end_date=start_date+timedelta(days=days)
    else:
        sys.exit(1)
    start_date=time_conversion(start_date)
    end_date=time_conversion(end_date)
    return {0:start_date,1:end_date}

def time_conversion(date):
    result=list(str(date))
    result[10]='T'
    result=''.join(result)+'Z'
    return result

def insert_values(cursor,data,table):
    placeholder=','.join(['%s']*len(data))
    columns=','.join(data.keys())
    sql="""
    INSERT INTO %s (%s)
    VALUES(%s)
    """%(table,columns,placeholder)
    cursor.execute(sql,list(data.values()))

def insert_values_primary(cursor,data,table,primary_key):
    placeholder=','.join(['%s']*len(data))
    columns=','.join(data.keys())
    key_placeholder=','.join(['{0}={1}.{0}'.format(k,table) for k in data.keys()])
    sql="""
    INSERT INTO %s (%s)
    VALUES (%s)
    """ %(table,columns,placeholder)
    cursor.execute(sql,list(data.values()))


if __name__=='__main__':
    main()
```

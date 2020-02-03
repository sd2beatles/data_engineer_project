# _Introduction_
Let's crawl data on the most popular K-pop groups registered at the Spotify website. The lists of singers can be obtained from Tumblr in 2019.
Since the site is an English-language site based in US, all the groups are selected based on the reputation in the country and reflect the American trends.

# _Steps_

![image](https://user-images.githubusercontent.com/53164959/73644936-a76c2d00-46b9-11ea-8acb-9d2c26700bc8.png)

Step 1) Put the data into csv.file 

![image](https://user-images.githubusercontent.com/53164959/73644985-bce15700-46b9-11ea-9cdf-2482a189eec4.png)

Step 2) Implement codes as it follows.

```python
import psycopg2 as ppg2
import six
import json
import os
import sys
import time
import requests
import six
import six.moves.urllib.parse as urllibparse
import base64
import logging
import pandas as pd
import csv

client_id="161975af6e9c43eaa63de06b51331fdb"
client_secret="ed8c9f468c924254aa2d2459246acba0"

def main():
    try:
        conn_string = "host='localhost' dbname ='postgres' user='postgres' password=1234 port=5432"
        conn = ppg2.connect(conn_string)
        cursor=conn.cursor()
    except:
        logging.error('Can not access the db')
        sys.exit(1)

    #create a list for string the artist_lists
    artists=[]
    with open('artist_lists.csv') as f:
        rows=csv.reader(f)
        for row in rows:
            artists.append(row[0])
    artists[0]='BTS'


    endpoint='https://api.spotify.com/v1/search'
    headers=get_headers(client_id,client_secret)
    for a in artists:
        params={
        'q':a,
        'type':'artist',
        'limit':1
        }
        r=requests.get(url=endpoint,params=params,headers=headers)
        raw=json.loads(r.text)
        artist=dict()
        #astrist_raw contains external_urls,followers,genres,href,id,images,name,popularity,type,url
        artist_raw=raw['artists']['items'][0]
        try:
            if artist_raw['name']==params['q']:
                artist.update({
                     'id':artist_raw['id'],
                     'name':artist_raw['name'],
                     'followers':artist_raw['followers']['total'],
                     'popularity':artist_raw['popularity'],
                     'url':artist_raw['uri']
                      })
                insert_values(cursor,artist,'artists')
        except:
             loggig.error("NO ITMES FOR SERACH API")
             continue
    # Exame if it works fine
    cursor.execute("SELECT * FROM artists;")
    result=cursor.fetchall()
    your_dataframe=pd.DataFrame(result)
    your_dataframe.columns=['id','name','followers','popularity','url']
    print(your_dataframe)
    #close the cursor to prevent any unnecessary leackage
    cursor.close()
    #close the connection
    conn.close()


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


def get_headers(client_id,client_secret):
    assert type(client_id)==str and type(client_secret)==str
    end_point='https://accounts.spotify.com/api/token'
    payload={'grant_type':'client_credentials'}
    encoded=base64.b64encode('{}:{}'.format(client_id,client_secret).encode('utf-8')).decode('ascii')
    header={"Authorization":"Basic {}".format(encoded)}
    r=requests.post(end_point,data=payload,headers=header)
    access_token=json.loads(r.text)['access_token']
    headers={'Authorization':"Bearer {}".format(access_token)}
    return headers

if __name__=='__main__':
    main()
```


![image](https://user-images.githubusercontent.com/53164959/73645140-1053a500-46ba-11ea-860b-f8abe0a77727.png)

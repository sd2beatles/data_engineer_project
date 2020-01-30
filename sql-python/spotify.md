
```sql
DROP TABLE IF EXISTS artists;
CREATE TABLE artists
(id VARCHAR(255) NOT NULL,
 name VARCHAR(255) NOT NULL,
 follower INT,
 popularity INT,
 url VARCHAR(255),
 iamge_url VARCHAR(255),
 PRIMARY KEY(id));
 
 CREATE TABLE artists_generes(
 artist_id VARCHAR(255),
 genre VARCHAR(255));
 
/*
If you want to convert the encoding,you should follow the below instruciton.

SHOW server_encoding;
SHOW client_encoding;

SET sever_encoding='UTF8'
SET client_encoding='UTF8'

SET client_encoding TO 
 */
``` 

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

client_id="161975af6e9c43eaa63de06b51331fdb"
client_secret="ed8c9f468c924254aa2d2459246acba0"


def main():
    try:
        conn_string = "host='localhost' dbname ='postgres' user='postgres' password=1234 port=5432"
        conn = ppg2.connect(conn_string)
        cursor=conn.cursor()
    except:
        logging.error('can not acces the db')
        sys.exit(1)

    headers=get_headers(client_id,client_secret)
    params={
        "q":"BTS",
        "type":"artist",
        "limit":4
    }

    r=requests.get("https://api.spotify.com/v1/search",params=params,headers=headers)
    if r.status_code!=200:
        logging.error(r.text)
        if r.status_code==429:
            retry=json.loads(r.headers)['Retry-After']
            time.sleep(int(retry))
            r=requests.get("https://api.spotify.com/v1/search",params=params,headers=headers)
        elif r.status_code==401:
            headers=get_headers(client_id,client_secrets)
            r=requests.get("https://api.spotify.com/v1/search",params=params,headers=headers)
        else:
            sys.exit(1)

    raw=json.loads(r.text)
    artist_raw=raw['artists']['items']
    for index in artist_raw:
            artists={
                'id':index['id'],
                'name':index['name'],
                'followers':index['followers']['total'],
                'popularity':index['popularity'],
                'url':index['external_urls']['spotify'],
                }
            insert_values(cursor,artists,table='artists',primary_key='id')
    cursor.execute('SELECT * FROM artists')
    result=cursor.fetchall()
    your_dataframe=pd.DataFrame(result)




def insert_values(cursor,data,table,primary_key):
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

if __name__=="__main__":
    main()


```

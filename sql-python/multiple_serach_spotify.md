## Introduction 

Let's visit the following website and import the data as text format. 

'https://github.com/fivethirtyeight/data/blob/master/classic-rock/classic-rock-song-list.csv


![image](https://user-images.githubusercontent.com/53164959/73843138-631b9100-4861-11ea-80ce-eec4127e1e6b.png)

The only column in which we are intrested is 'artist name' and we will retrieve the associated information for each artists from the s
spotify API. The final result is to be stored as the separate file in csv format. 


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
import pathlib


client_id="161975af6e9c43eaa63de06b51331fdb"
client_secret="ed8c9f468c924254aa2d2459246acba0"
host='https://github.com/fivethirtyeight/data/blob/master/classic-rock/classic-rock-song-list.csv'

def main():
    try:
        conn_string = "host=localhost dbname =postgres user=postgres password=1234 port=5432"
        conn = ppg2.connect(conn_string)
        cursor=conn.cursor()
    except:
        logging.error('Can not access the db')
        sys.exit(1)
    data=load_data('artists.txt')
    data=data.iloc[:,:8]
    data.columns=['song','artist','release_year','combined','first','year','plycount','fg']
    #remove the duplicate artists
    artist=data['artist'].unique()
    headers=get_headers(client_id,client_secret)
    url='https://api.spotify.com/v1/search'
    for a in artist:
        params={
        'q':a,
        'type':'artist',
        'limit':1
        }
        r=requests.get(url=url,params=params,headers=headers)
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
        artists={}
        #from artist_raws, we extract   external_urls,followers,genres,href,id,images,name,popularity,type,url,generes
        try:
            artist_raw=raw['artists']['items'][0]
            artists.update({
                 'id':artist_raw['id'],
                 'name':artist_raw['name'],
                 'followers':artist_raw['followers']['total'],
                 'popularity':artist_raw['popularity'],
                 'url':artist_raw['uri'],
                 'genres':','.join(artist_raw['genres'])
                 })
            insert_values(cursor,artists,'artists')
        except:
            logging.error('No items from serach api')
            continue
    fileName='artists.csv'
    export_to_csv(cursor,fileName,'artists')



def export_to_csv(cursor,fileName,tableName,filePath=None):
    assert type(fileName) ==str and type(tableName)==str
    try:
        if filePath is None:
            filePath=str(pathlib.Path().absolute())+'\\'
        sql="SELECT * FROM {}".format(tableName)
        cursor.execute(sql)
        results=cursor.fetchall()
        headers=[i for i in cursor.description]
        csvFile=csv.writer(open(filePath+fileName,'w',newline='',encoding='utf-8'),delimiter=',',lineterminator='\r\n',escapechar='\\')
        #Add the headers and data to the csv fileName
        csvFile.writerow(headers)
        csvFile.writerows(results)
        #message
        print("Data Export Successful.")
    except ppg2.DatabaseError as e:
        print("Data Export Unsuccessful")


def load_data(file):
    data=[]
    with open(file,mode='r',encoding='utf-8') as f:
        for index,line in enumerate(f.readlines()):
            if index==0:
                pass
            else:
                data.append(line.replace('\n','').split(','))
    data=pd.DataFrame(data)
    return data


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

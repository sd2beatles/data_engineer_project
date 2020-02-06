## Introduction 

The Spotify prodives a special feature to retrieve a batch infomration of artists up to max 50 for a indiviual request. 
This flexible and convenience feature allows the users to reduce the time spending on collecting data from api and preventing the overlaoding 
in the server. Let's write a simple code. 

```python
import psycopg2 as ppg2
import json
import os
import requests
import logging

i

file='artists.csv'
data=pd.read_csv(file,sep=',')
artist_id=data.iloc[:,0]

client_id="161975af6e9c43eaa63de06b51331fdb"
client_secret="ed8c9f468c924254aa2d2459246acba0"

def main():
    artists_batch=[artist_id[i:i+50] for i in range(0,len(artist_id),50)]
    headers=get_headers(client_id,client_secret)
    for group in artists_batch:
        ids=','.join(group)
        url='https://api.spotify.com/v1/artists'
        params={'ids':ids}
        r=requests.get(url,params=params,headers=headers)
        #raw is a listy consting of 50 artists
        raws=json.loads(r.text)['artists']
    

            
            
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

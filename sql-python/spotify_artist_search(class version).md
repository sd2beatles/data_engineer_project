

###1.Python Note:

#### 1.1 Environmental Variable

|Content |Code|Example|
|-------|---- |-------|
| Create an environmental variable|```$env:environmental_name=environmental_value```| $env:clinet_id='asdfasf123'|
| Call up the specific environmental variables|```Get-ChildItem env:env_name,env:env_name```|Get-ChildItem env:cleint_id|
|Remove the variables|```Step 1) After writing up to "Remove-Item env:", double taps and choose the variable you want to delete.  Step 2) Check if your code follows the next template,Remove-Item Env:\env_name.``` | Remove-Item Env:\client_id,Env:\client_secrets|

#### 1.2 postgresql 

```python
    If you want to use postgresql, then try the following code below
    try:
        conn_string = "host='localhost' dbname ='postgres' user='postgres' password=1234 port=5432"
        conn = ppg2.connect(conn_string)
        cursor=conn.cursor()
    except:
        logging.error('can not acces the db')
        sys.exit(1)
```

### 2. Code


```python
import numpy as np
import base64
import os
import sys
import requests
import time
import json
import psycopg2
import mysql.connector
import logging
from mysql.connector import errorcode



client_id="161975af6e9c43eaa63de06b51331fdb"
client_secret="ed8c9f468c924254aa2d2459246acba0"


class SpotifyOuathError(Exception):
    pass



def get_headers(client_id,client_secret):
    encoded=base64.b64encode("{}:{}".format(client_id,client_secret).encode('utf-8')).decode('ascii')
    header={"Authorization":"Basic {}".format(encoded)}
    return header


class SpotifiyClinetInfo(object):
    authorization_url="https://accounts.spotify.com/api/token"

    def __init__(self,client_id=None,client_secret=None,artists=None,cursor=None,saving_mode='mysql'):
        '''
        Artists can be anything whose tpye is similar to a single vector. Also one single string is also possible.
        However, maxtrix type inputs are denied in time.
        '''

        assert saving_mode in ['mysql','postgresql'],"Saving mode must be one of mysql and postgresql"
        if not client_id:
            client_id=os.getenv('client_id')
        if not client_secret:
            client_secret=os.getenv('client_secret')
        if not client_id:
            raise SpotifyOuathError("No client_id")
        if not client_secret:
            raise SpotifyOuathError("No client_secret")
        self.client_id=client_id
        self.client_secret=client_secret
        self.artists=artists
        #In the previous seciton,we preapred a talbe called artists whose id value is primary Keys
        #Duplicate entires lead to unwanted errors.
        if artists!=None:
            unique_artists=set(artists)
            if len(unique_artists)==len(artists):
                self.artists=artists
            else:
                self.artists=unique_artists
        self.cursor=cursor
        assert saving_mode in ['mysql','postgresql'],"saving_mode must either mysql or postgresql"
        self.saving_mode=saving_mode

    def get_accessToken(self):
        headers=get_headers(self.client_id,self.client_secret)
        payload={"grant_type":"client_credentials"}
        r=requests.post(self.authorization_url,data=payload,headers=headers)
        #to return json format and only extract the required value(ie) access_token
        raw=r.json()['access_token']
        return raw

    def get_artist_save(self):
        access_token=self.get_accessToken()
        headers={"Authorization":"Bearer {}".format(access_token)}
        for a in self.artists:
            params={'q':a,
                    'type':'artist',
                    'limit':1}
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
            #from artist_raws, we extract   external_urls,followers,genres,href,id,images,name,popularity,type,url,generes
            artists={}
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

            except:
                logging.error('No items from serach api')
                continue
            self.insert_row(data=artists,table='artists')

    def insert_row(self,data,table):
        placeholder=','.join(['%s']*len(data))
        columns=','.join(data.keys())
        sql="INSERT INTO %s (%s) VALUES (%s)" %(table,columns,placeholder)
        #duplicate values needed, one for placeholders and the other for keyholder.
        self.cursor.execute(sql,list(data.values()))



def main():
    artists=['BTS','twice']
    try:
         conn = mysql.connector.connect(host='localhost', port='3306', database='spotify', user='root', password='1234', charset='utf8')
         cursor=conn.cursor()
    except mysql.connector.Error as e:
        print(e)

    SpotifiyClinetInfo(client_id=client_id,client_secret=client_secret,artists=artists,cursor=cursor).get_artist_save()
    conn.commit()
  

if __name__=="__main__":
    main()
```

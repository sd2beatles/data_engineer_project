
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
client_id='161975af6e9c43eaa63de06b51331fdb'
client_secret='5c707c00e6de4441a82d142e74dfaa5a'

def get_headers(clien_id,client_secret):
   encoded=base64.b64encode("{}:{}".format(client_id,client_secret).encode('utf-8')).decode('ascii')
   header={"Authorization":"Basic {}".format(encoded)}
   return header

class spotfiySearch(object):
    
    def __init__(self,client_id,client_secret,artists,cursor):
        self.client_id=client_id
        self.client_secret=client_secret
        #to avoid having the same artists in the list
        if artists!=None:
            unique_artists=set(artists)
            if len(artists)==len(unique_artists):
                self.artists=artists
            else:
                self.artists=unique_artists
        self.cursor=cursor
   
    def get_accessToken(self):
        headers=get_headers(self.client_id,self.client_secret)
        payload={"grant_type":"client_credentials"}
        url=' https://accounts.spotify.com/api/token'
        r=requests.post(url,headers=headers,data=payload)
        raw=r.json()['access_token']
        return raw
    
    def get_artists_save(self,tb_name): #tb_name indicates the table name
        access_token=self.get_accessToken()
        headers={'Authorization':'Bearer {}'.format(access_token)}
        for a in self.artists:
            params={
                'q':a,
                'type':'artist',
                'limit':'1'}
            r=requests.get("https://api.spotify.com/v1/search",params=params,
                           headers=headers)
            if r.status_code==429:
                retry=json.loads(r.headers)['Retry-After']
                time.sleep(int(retry))
                r=requests.get("https://api.spotify.com/v1/search",params=params,
                           headers=params)
            elif r.status_code==401:
                headers=get_headers(self.client_id,self.client_secrets)
                r=requests.get("https://api.spotify.com/v1/search",params=params,headers=headers)
           
            raw=json.loads(r.text)
            artist={}
            try:
                artist_raw=raw['artists']['items'][0]
                artist.update({
                    'id':artist_raw['id'],
                    'name':artist_raw['name'],
                    'followers':artist_raw['followers']['total'],
                    'popularity':artist_raw['popularity'],
                    'genres':str(artist_raw['genres'])})
            except:
                logging.error('No infomration of the artist is found')
                continue
            placeholder=','.join(['%s']*len(artist))
            columns=','.join(artist.keys())
            sql="insert into %s (%s) values (%s)" %('artists',columns,placeholder)
            self.cursor.execute(sql,list(artist.values()))
    
        
    sdf
            
            
def main():
    artists=['BTS']
    try:
        conn=pymysql.connect(host='localhost',user='root',port=3306,db='production',passwd='1234',charset='utf8')
        cursor=conn.cursor()
    except:
        logging.error('Connection failed')
    spotfiySearch(client_id,client_secret,artists,cursor).get_artists_save(tb_name='artists')
    conn.commit()
    
    
if __name__=='__main__':
    main()



```


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
#Connect to internal database
client_id="161975af6e9c43eaa63de06b51331fdb"
client_secrets="ed8c9f468c924254aa2d2459246acba0"


def main():
    try:
        conn = ppg2.connect("host = localhost dbname=postgres user=postgres password=1234 port=5432")
        conn.autocommit = True
        cursor=conn.cursor()
    except:
        logging.error('can not access')
        exit(1)

    headers=get_headers(client_id,client_secrets)
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
    print(raw['artists'].keys())
    #we can see what keys are in the raw['artists']['items']
    print(raw['artists']['items'][0].keys())
    #now create a dict
    artist_raw=raw['artists']['items'][0]
    if artist_raw['name']==params['q']:
        artist={
        'id':artist_raw['id'],
        'name':artist_raw['name'],
        'follower':artist_raw['followers']['total'],
        'popularity':artist_raw['popularity'],
        'url':artist_raw['external_urls']['spotify'],
        'image_url':artist_raw['images'][0]['url']
        }


    def insert_row(cursor,data,table,primary_key):
        #assert type(data)==dict
        placeholder=','.join(['%s']*len(data)) #equailvalent to ('{}','{}','{}','{}','{}','{}')
        #make sure that you have to match the keys to columns of table, otherwise causing errors.
        columns=','.join(data.keys())
        key_placeholders=','.join(['{0}={1}.{0}'.format(k,table) for k in data.keys()])
        sql="INSERT INTO %s (%s) VALUES (%s) ON CONFLICT (%s) DO UPDATE SET %s" %(table,columns,placeholder,primary_key,key_placeholders)
        cursor.execute(sql,list(data.values()))

    '''
    query="""
    INSERT INTO artists (id,name,follower,popularity,url,image_url)
    VALUES('{}','{}','{}','{}','{}','{}')
    ON CONFLICT (id) DO UPDATE SET id=artists.id,name=artists.name,follower=artists.follower,popularity=artists.popularity,url=artists.url,image_url=artists.image_url
    """.format(
    artist['id'],
    artist['name'],
    artist['followers'],
    artist['popularity'],
    artist['url'],
    artist['image_url'])
    '''

def get_headers(client_id,client_secrets):
    endpoint='https://accounts.spotify.com/api/token'
    encoded=base64.b64encode("{}:{}".format(client_id,client_secrets).encode('utf-8')).decode('ascii')
    headers={
    "Authorization": "Basic {}".format(encoded)
    }
    payload={
    "grant_type":"client_credentials"
    }
    r=requests.post(endpoint,data=payload,headers=headers)
    access_token=json.loads(r.text)['access_token']
    #print access_token
    headers={"Authorization":"Bearer {}".format(access_token)}
    return headers




if __name__=='__main__':
    main()
```

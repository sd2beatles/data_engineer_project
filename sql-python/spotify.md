
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




def main():
    con=psycopg2.connect(
      host='localhost',
      database='postgres',
      user='postgres',
      password=1234,
      port=5432)
    cursor=con.cursor()
    print(cursor.execute('select 1;'))
    sys.exit(0)
    try:
        con=psycopg2.connect(
          host='localhost',
          database='postgres',
          user='postgres',
          password=1234,
          port=5432)
        cursor=con.cursor()

    except:
        logging.error("Can not access to RDS")
        exit(1)



    headers=get_headers(client_id,client_secrets)
    params={
        "q":"BTS",
        "type":"artist",
        "limit":1
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
        'followers':artist_raw['followers']['total'],
        'popularity':artist_raw['popularity'],
        'url':artist_raw['external_urls']['spotify'],
        'image_url':artist_raw['images'][0]['url']
        }
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

    cursor.execute(query)
    sys.exit(0)

    #you should set up the codes for the information you want
    total=raw['total']
    offset=raw['offset']
    next=raw['next']


    #create a list to store information on items
    albums=[]
    albums.extend(raw['items'])
    #check out the number of albumns equal to 20
    print(len(albums))

    #if you want to store the alumbs up to a specifiy number
    count=0
    #note that raw['next'] returns none if url is not available.
    #While loops still iterate over if cout is less than 100 and next is avilable
    while count<100 and next:
        r=requests.get(raw['next'],headers=headers)
        raw=json.loads(r.text)
        next=raw['next']
        print(next)
        albums.extend(raw['items'])
        count=len(albums)
    print(len(albums))

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

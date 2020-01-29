
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

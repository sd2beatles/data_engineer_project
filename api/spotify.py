#!/usr/bin/env python
# coding: utf-8

# In[9]:


import numpy as np
import six
import json
import os
import sys
import time
import requests
import six
import six.moves.urllib.parse as urllibparse
import base64


# ## Step 1) Set up Authorization and Get access Code
# 
# ![image](https://user-images.githubusercontent.com/53164959/72664750-e147fd00-3a44-11ea-86da-c95e6b75d33a.png)
# 
# 
# ![image](https://user-images.githubusercontent.com/53164959/72664507-1b63cf80-3a42-11ea-9851-4e94ff9a4a55.png)
# 
# 
# 1

# In[16]:


import sys
import requests
import base64
import json
import logging



client_id="161975af6e9c43eaa63de06b51331fdb"
client_secret="ed8c9f468c924254aa2d2459246acba0"

def main():
    endpoint='https://accounts.spotify.com/api/token'
    encoded=base64.b64encode("{}:{}".format(client_id,client_secret).encode('utf-8')).decode('ascii')
    headers={
    "Authorization": "Basic {}".format(encoded)
    }
    payload={
    "grant_type":"client_credentials"
    }
    r=requests.post(endpoint,data=payload,headers=headers)
    print(r.text)
    print(type(r))
    sys.exit(0)


if __name__=='__main__':
    main()


# ### * Keys To Remember 
# 
# 1) The outcome is following below and we should see that the output type is string. The only information we extract from r is 'access code.' To get the information,we first need to convert the string data into dictionary format. This can be done trhouhg the package called 
# json.loads
# 
# 2) After undergoing the first step, we are now seeing that the access_token is now dict but the key of value which we want to obtain is 
#    'access_token'. Let the code write as  json.loads(r.text)['access_token']

# In[17]:


def main():
    endpoint='https://accounts.spotify.com/api/token'
    encoded=base64.b64encode("{}:{}".format(client_id,client_secret).encode('utf-8')).decode('ascii')
    headers={
    "Authorization": "Basic {}".format(encoded)
    }
    payload={
    "grant_type":"client_credentials"
    }
    r=requests.post(endpoint,data=payload,headers=headers)
    print(r.text)
    #access_token=json.loads(r.text)['access_token']
    #print access_token
    #print(access_token)
    sys.exit(0)
    
if __name__=='__main__':
    main()
    


# ## Step 2 Use the token to access the spotify Web Api
# 
# ![image.png](attachment:image.png)
# 
# 
# ### * key Note
# 
# We define a separate function called get_headers and implment it in main function. 
# 
# 
# 

# In[18]:


client_id="161975af6e9c43eaa63de06b51331fdb"
client_secrets="25eea1c24fc649c4850d5871fa84ae8b"

def main():
    headers=get_headers(client_id,client_secrets)
    print(headers)

    
def get_headers(client_id,client_secrets):
    endpoint='https://accounts.spotify.com/api/token'
    encoded=base64.b64encode("{}:{}".format(client_id,client_secret).encode('utf-8')).decode('ascii')
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


# ## Step 3. Search API

# ### To obatin the infomration about albums,atrists you are interested in, we should follow the assigned instruciton below. 
# 
# ![image](https://user-images.githubusercontent.com/53164959/72665191-22daa700-3a49-11ea-9da2-6a95b42e8d87.png)
# 
# 
# ### * Key Noetes
# 
# There are a number of query parameters in order to get the accurate search infomration. We will assign some of them. 
# 
# ![image](https://user-images.githubusercontent.com/53164959/72665266-f96e4b00-3a49-11ea-9ef8-4539100c4080.png)
# 

# In[19]:


client_id="161975af6e9c43eaa63de06b51331fdb"
client_secrets="25eea1c24fc649c4850d5871fa84ae8b"

def main():
    headers=get_headers(client_id,client_secrets)
    params={
        "q":"BTS",
        "type":"artist",
        "limit":5
    }
    #request.get("authorization",query_param,headers)
    r=requests.get("https://api.spotify.com/v1/search",params=params,headers=headers)
    print(r.text)
if __name__=='__main__':
    main()


# # 2. Error Handling

# #### In this section, we will explore a way to deal with the issues associated with API errors. If hoping to look into more specific error codes, you can visit the following web site. 
# 
# 
# 
# ![image.png](attachment:image.png)
# 

# In[39]:


def main():
    headers=get_headers(client_id,client_secrets)
    params={
        "q":"BTS",
        "type":"artist",
        "limit":5
    }
    try:
        r=requests.get("https://api.spotify.com/v1/search",params=params,headers=headers)
    except:
        logging.error(r.text)
        sys.exit(1)
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
            
   
    
if __name__=='__main__':
    main()


# ![image.png](attachment:image.png)
# 

# ## 3.Paging 

# ![image.png](attachment:image.png)
# 
# 
# ## Note
# The serach result may contain a vast of information distrupting the server and leaind to a temporary block or errors. In order to prevent this from happening, spotify provided a unique feature so called pagination. You may simply remember it as segmenation of the whole information. 

# #### 3.1 Get Basic Information

# In[59]:


def main():
    headers=get_headers(client_id,client_secrets)
    params={
        "q":"BTS",
        "type":"artist",
        "limit":5
    }
    try:
        r=requests.get("https://api.spotify.com/v1/search",params=params,headers=headers)
    except:
        logging.error(r.text)
        sys.exit(1)
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
            
    '''
    Key to remember:
    You must first get the unique id.The relevant information is available from 'id' in r.text
    
    '''
    r=requests.get("https://api.spotify.com/v1/artists/3Nrfpe0tUJi4K4DXYWgMUX/albums",headers=headers)
    raw=json.loads(r.text)
    
    #you should set up the codes for the information you want 
    total=raw['total']
    offset=raw['offset']
    next=raw['next']
    #the total number of albumns of the interested artist
    print(total)
    #current url page number
    print(offset)
    #next url page address
    print(next)
    
    
    
if __name__=='__main__':
    main()


# ![image.png](attachment:image.png)

# ### 3.2 Store Albums

# In[66]:


def main():
    headers=get_headers(client_id,client_secrets)
    params={
        "q":"BTS",
        "type":"artist",
        "limit":5
    }
    try:
        r=requests.get("https://api.spotify.com/v1/search",params=params,headers=headers)
    except:
        logging.error(r.text)
        sys.exit(1)
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
            
    '''
    Key to remember:
    You must first get the unique id.The relevant information is available from 'id' in r.text
    
    '''
    r=requests.get("https://api.spotify.com/v1/artists/3Nrfpe0tUJi4K4DXYWgMUX/albums",headers=headers)
    raw=json.loads(r.text)
    
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
    
    
        
if __name__=='__main__':
    main()


# ![image.png](attachment:image.png)

# In[ ]:





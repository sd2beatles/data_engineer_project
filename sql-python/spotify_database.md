![image](https://user-images.githubusercontent.com/53164959/83850098-5cd3ed80-a74b-11ea-821a-e712eed20ee0.png)






## 1. Access token 받는 법

![image](https://user-images.githubusercontent.com/53164959/83963982-a277ee00-a8e4-11ea-921f-11352225e1ad.png)
![image](https://user-images.githubusercontent.com/53164959/83963450-4069b980-a8e1-11ea-97dc-218c34c8d12f.png)

- endpoint 는 url  https://accounts.spotify.com/api/token 임을 알 수 있다. Post를 사용할 것
- post request에 다음과 같은 grand_type=client_credentials 인 parameter를 집어넣어야 한다. -d 이므로 python requests.post의 data에 집언넣음
- post request에 'Authorization: Basic {decode}'를 paramter로 집어넣어야 함. 이때 -h이므로 header항목에 넣는다.
  또한 추가적으로 decode는 client_id,self.client_secret를 endcoe64로 전환한 후에 집어넣어야 한다. 
  
  코드를 구현하면 아래와 같다.
```python
  def get_headers(client_id,client_secret):
    encoded=base64.b64encode("{}:{}".format(client_id,client_secret).encode('utf-8')).decode('ascii')
    header={"Authorization":"Basic {}".format(encoded)}
    return header



def get_access_token(client_id_id,client_secret):
    headers=get_headers(client_id,client_secret)
    payload={'grant_type':'client_credentials'}
    url=' https://accounts.spotify.com/api/token'
    r=requests.post(url,data=payload,headers=headers)
    raw=r.json()['access_token']
    return raw
   
raw=get_access_token(client_id,client_secret)
print(raw)
```


## 2.search 

Visit the following website https://developer.spotify.com/documentation/web-api/reference/search/search/
![image](https://user-images.githubusercontent.com/53164959/83964443-2c758600-a8e8-11ea-9b48-04c47e7b635f.png)
![image](https://user-images.githubusercontent.com/53164959/83964464-4adb8180-a8e8-11ea-99ca-c65a16808418.png)

end point 즉 url이 



  

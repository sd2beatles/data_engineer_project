import os
import sys
import urllib.request
import requests
import urllib.request
import urllib.error
import urllib.parse
from bs4 import BeautifulSoup
import sys
import json
import math
import re
client_id='mGheSDZSqWyhMF5gFAqU'
client_secrets='i3HQTMe9Sx'

def get_blog_count(query,display):
    encText = urllib.parse.quote(query)
    search_url = "https://openapi.naver.com/v1/search/blog?query=" + encText
    request=urllib.request.Request(search_url)
    request.add_header('X-Naver-Client-Id',client_id)
    request.add_header('X-Naver-Client-Secret',client_secrets)
    #request acess to web api
    response=urllib.request.urlopen(request)
    #get status to see if our code is working fine
    response_code=response.getcode()

    if response_code==200:
        response_body=response.read()
        #to convert response_body into json format
        response_body_dict=json.loads(response_body.decode('utf-8'))
        '''
        keys are composed of lastBuildDate,total,start,display,items
        if you want to print out the corresponding values for the key,
        try the below codes

        print('Last Build Date'+response_body_dict['lastBuildDate'])
        print('Total:'+response_body_dict['total'])
        print('Start:'+response_body_dict['start'])
        print('Display'+response_body_dict['display'])
        '''
        if response_body_dict['total']==0:
            blog_count=0
        else:
            blog_total=math.ceil(response_body_dict['total']/int(display))
            if blog_total>=1000:
                blog_count=1000
            else:
                blog_count=blog_total
    return blog_count



def get_blog_post(query,display,start_index,sort):
    global no,fs
    encText = urllib.parse.quote(query)
    search_url = "https://openapi.naver.com/v1/search/blog?query=" + encText+'&display='+str(display)+'&start='+str(start_index)+'&sort='+sort
    request=urllib.request.Request(search_url)
    request.add_header('X-Naver-Client-Id',client_id)
    request.add_header('X-Naver-Client-Secret',client_secrets)
    response=urllib.request.urlopen(request)
    response_code=response.getcode()
    if response_code is 200:
        response_body=response.read()
        response_body_dict=json.loads(response_body.decode('utf-8'))
        for item_index in range(0,len(response_body_dict['items'])):
            try:
                #remove any tags
                remove_html_tag=re.compile('<.*?>')
                title=re.sub(remove_html_tag,'',response_body_dict['items'][item_index]['title'])
                #filter out unnecessary letters
                link=response_body_dict['items'][item_index]['link'].replace('amp;','')
                description=re.sub(remove_html_tag,'',response_body_dict['itmes'][item_index]['description'])
                blogger_name=response_body_dict['items'][item_index]['bloggername']
                blogger_link=response_body_dict['items'][item_index]['bloggerlink']
                post_date=response_body_dict['itmes'][item_index]['postedate']
                no+=1
                print("-"*100)
                print("#"+str(no))
                print("Title:"+title)
                print("Link:"+link)
                print("Description:"+description)
                print("Blogger_name:"+blogger_name)
                print("Bloggger_link:"+blogger_link)
                print("Post Date:"+post_date)

                #now we are ready to obtain the content posted on each blog_count
                post_code=requests.get(link)
                post_text=post_code.text
                post_soup=BeautifulSoup(post_text,'lxml')
                #Naver uses iframe to limit ceartain access including copying or screen captures
                #In this case, we should travel a quite long and repetitive codes to get the 'real' contents
                for mainFrame in post_soup.select("iframe#mainFrame"):
                    blog_post_url="http://blog.naver.com"+mainFrame.get('src')
                    blog_post_code=requsts.get(blog_post_url)
                    blog_post_text=blog_post_code.text
                    blog_post_soup=BeautifulSoup(blog_post_text,'lxml')

                    for blog_post_content in blog_post_soup.select('div#postViewArea'):
                        blog_post_conte_text=blog_post_content.get_text()
                        blog_post_full_contents=str(blog_post_content_text)
                        blog_post_full_contents=blog_post_full_contents.replace('\n\n','\n')
                        fs.write(blog_post_full_contents+"\n")
                        fs.write('--'*100)


            except:
                item_index+=1

if __name__=='__main__':
    no=0
    #fllowings are request pareameters
    query='BTS'
    #set up the number of display to 10 per search
    display=10
    #start ranges from 1 to 1000
    start=1
    #there are two options to sort our seraches by either sim or date
    sort='date'
    fs=open(query+'.txt','a',encoding='utf-8')
    blog_count=get_blog_count(query,display)
    for start_index in range(start,blog_count+1,display):
        get_blog_post(query,display,start_index,sort)
    fs.close()

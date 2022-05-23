#importing all dependencies
from operator import index
import unicodedata
from h11 import Data
import numpy as np
from pkg_resources import yield_lines
#import tweepy
import requests
import base64
import pandas as pd
import json 

#Define your keys from the developer portal
consumer_key = '6YZtW8dT3vBEjaIEkQ16I0rQi'
consumer_secret = 'MoTJ4lvDCXUIXGnNSTa7WwtkSfNmPSdTJ9m68LRWvxtb8F5xgE'

#Reformat the keys and encode them
key_secret = '{}:{}'.format(consumer_key, consumer_secret).encode('ascii')
#Transform from bytes to bytes that can be printed
b64_encoded_key = base64.b64encode(key_secret)
#Transform from bytes back into Unicode
b64_encoded_key = b64_encoded_key.decode('ascii')

base_url = 'https://api.twitter.com/'
auth_url = '{}oauth2/token'.format(base_url)
auth_headers = {
    'Authorization': 'Basic {}'.format(b64_encoded_key),
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
}
auth_data = {
    'grant_type': 'client_credentials'
}
auth_resp = requests.post(auth_url, headers=auth_headers, data=auth_data)
print(auth_resp.status_code)
access_token = auth_resp.json()['access_token']




trend_headers = {
    'Authorization': 'Bearer {}'.format(access_token)    
}

trend_params = {
    'id':23424768 ,
}

trend_url = 'https://api.twitter.com/1.1/trends/place.json'  
trend_resp = requests.get(trend_url, headers=trend_headers, params=trend_params)


tweet_data = trend_resp.json()
#print(tweet_data[0])


#for i in range(0,10):
#Quantidade de Tweets Buscadas
i=10
geral=[]
row=''
while(i>0):
  #print(tweet_data[0]['trends'][i])
  #print('')
  #print('')
  #print('')
  #print('')
  #print('')
  name = tweet_data[0]['trends'][i]['name']
  url = tweet_data[0]['trends'][i]['url']
  tweetVolume = tweet_data[0]['trends'][i]['tweet_volume']
  row={'nome': name,'url':url,'qtde':tweetVolume}
  geral.append(row)
  i=i-1
print (geral)
  


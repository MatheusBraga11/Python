from asyncio.windows_events import NULL
from concurrent.futures import process
from encodings.utf_8_sig import encode
from urllib import response, robotparser
from urllib.parse import urlencode
from wsgiref.util import request_uri
import scrapy
import requests
import re 
import pandas as pd
import csv
import pyspark
import nltk
import pandas as pd
from pyspark.sql import SparkSession
from nltk.tokenize import word_tokenize
from unidecode import unidecode
from pyspark import SparkContext, SparkConf
import pyspark.sql.functions as f

# Imports the Google Cloud client library
from google.cloud import storage
class SpidergazetaSpider(scrapy.Spider):
    name = 'spidergazeta'
    #allowed_domains = ['www.gazetadopovo.com.br']
    start_urls = ['https://www.gazetadopovo.com.br/tudo-sobre/gazeta-noticias/']

    def parse(self, response):
        totalpag = response.css('div.wrapper.pagination').css('span::text').getall()
        totalpag=int(re.sub("1 de ",'',totalpag[0]))
        tutloconc=[]
        while (totalpag>0):
            if totalpag==1:
                url=''
                url = response.urljoin(url)
            else:
                url=str(totalpag)+'/'
                url = response.urljoin(url)
            totalpag = totalpag-1
            row={'totalpag': totalpag}
            if url is not None:
                yield scrapy.Request(url=url,callback=self.demaispag,meta=row)        
    
    def demaispag(self,response):
       row=[]
       header='noticia'
       for noticias in response.css("article.article-item.has-image "):
            titulo = noticias.css('h2::attr(title)').get().replace('"','')
            #row = {'titulo': titulo}
            #yield row
            row.append(titulo)
       print(row)     
       with open('gazeta.csv','w' ,encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=',',lineterminator = '\n')
            writer.writerow([header])
            for rows in row:
                writer.writerow([rows])
	# Instantiates a client
       storage_client = storage.Client()
       meubucket="bigdataavaliacao"
       #bucket = str(storage_client.get_bucket(meubucket))
       try:
                bucket = storage_client.create_bucket(meubucket)
                print(f"Bucket {bucket.name} created.")
#subir arquivo
       except:
                print("Bucket já existe")
       storage_client = storage.Client()
       bucket = storage_client.bucket(meubucket)
       path=r"C:\Users\Matheus\projetogazeta\gazeta.csv"
       name="Gazeta"
       blob = bucket.blob(name)

       blob.upload_from_filename(path)

       print(f"File {path} uploaded to {name}.")

       print(f"File {path} uploaded to {name}.")
       
       

       
        
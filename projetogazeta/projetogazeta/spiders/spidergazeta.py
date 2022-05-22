from asyncio.windows_events import NULL
from concurrent.futures import process
from urllib import response, robotparser
from urllib.parse import urlencode
from wsgiref.util import request_uri
import scrapy
import requests
import re 
import pandas as pd

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
       for noticias in response.css("article.article-item.has-image "):
            titulo = noticias.css('h2::attr(title)').get().replace('"','')
            row = {'titulo': titulo}
            yield row


       
        
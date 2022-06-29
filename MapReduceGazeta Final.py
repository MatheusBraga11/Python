#! /usr/bin/python
from pyspark.sql import SparkSession
import pyspark.sql.functions as f
from pyspark.ml import *
from pyspark.ml.feature import *
from pyspark.ml.feature import HashingTF, IDF, Tokenizer
from pyspark.sql.functions import *
from pyspark.sql.functions import col, concat_ws

appName = "PySpark Example - Read JSON file from GCS"
master = "local"

print('inicio...')
# Create Spark session
spark = SparkSession.builder \
    .appName(appName) \
    .master(master) \
    .getOrCreate()

#LENDO DO BUCKET O ARQUIVO GERADO#
#Para quando rodar no servidor
arquivo_bucket = "gs://bigdataavaliacao/Gazeta"

noticiasDF = spark.read.option("header",True).csv(arquivo_bucket,encoding=('utf-8'))



# Removendo Stop Words
stop = ['os','a','e','i','de','do','que','é','da','o',' o','as','   ','em','sem','no']
stop = [l.lower() for l in stop]

tokenizer = Tokenizer(inputCol="noticia", outputCol="words")
wordsData = tokenizer.transform(noticiasDF)

remover = StopWordsRemover(inputCol="words", outputCol="noticiafit",stopWords = stop)
get_remover = remover.transform(wordsData)

#Tira o array da coluna do data frame e transforma em um texto (Muito Tooop)
dffinal = get_remover.withColumn("noticiafit2",
   concat_ws(",",col("noticiafit")))
#dffinal.show()
dffinal = dffinal.drop("noticia","words","noticiafit") 
dffinal = dffinal.withColumn('noticiafit2', regexp_replace('noticiafit2', ',', ' '))
dffinal.show()

#Map Reduce
dffinal.withColumn('word', f.explode(f.split(f.col('noticiafit2'), ' ')))\
    .groupBy('word')\
    .count()\
    .sort('count', ascending=False)\
    .show()

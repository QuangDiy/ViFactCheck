import psycopg2, pickle
# from fastapiapp.BM25 import BM25Okapi
from BM25 import BM25Okapi
import numpy as np

import pandas as pd
from minio import Minio

def get_minio_client():
    client = Minio("localhost:9000", "R3rjkgjN6Qmla2RLMrhl", "kwvrweMHmD3I5qyci9tQ6URWH2Y39y1GHOpIPo64", secure=False)
    return client

def search_bm25(query, connection):

    cursor = connection.cursor()
    cursor.execute("SELECT content FROM news")
    datacorpus = cursor.fetchall()

    df = pd.DataFrame(datacorpus, columns=['content'])
    corpus = df['content'].tolist()

    connect = get_minio_client()

    file = connect.get_object(bucket_name="bm25model",object_name="bm25.pkl")

    # try:
    #     file = connect.get_object(bucket_name="bm25model",object_name="bm25.pkl").read()
    # finally:
    #     file.close()
    bm25 = pickle.load(file)

    tokenized_query = query.split(" ")

    bm25_output = bm25.get_top_n(tokenized_query, corpus, n = 1)
    doc_scores = bm25.get_scores(tokenized_query)


    bm25_output = ''.join(bm25_output)
    sql_query = "SELECT url FROM news WHERE content = %s"
    cursor.execute(sql_query, (bm25_output,))
    url = cursor.fetchall()
    url = url[0][0]

    cursor.close()
    connection.close()

    return bm25_output,url

# def request_url(context, connection):
#     cursor = connection.cursor()
#     sql_query = "SELECT url FROM news WHERE content = %s"
#     cursor.execute(sql_query, (context,))
#     url = cursor.fetchall()
#     url = url[0][0]
#     cursor.close()
#     connection.close()
#     return url

# def search_bm25(query, connection):
#     cursor = connection.cursor()
#     cursor.execute("SELECT content FROM news")
#     datacorpus = cursor.fetchall()

#     df = pd.DataFrame(datacorpus, columns=['content'])
#     corpus = df['content'].tolist()

#     # Save bm25
#     # tokenized_corpus = [str(doc).split(" ") for doc in corpus]
#     # bm25 = BM25Okapi(tokenized_corpus)
    
#     # with open("bm25.pkl", "wb") as file:
#     #     pickle.dump(bm25, file)

#     # load Bm25
#     with open("bm25.pkl", "rb") as file:
#         bm25 = pickle.load(file)

#     tokenized_query = query.split(" ")

#     # doc_scores = bm25.get_scores(tokenized_query)
#     bm25_output = bm25.get_top_n(tokenized_query, corpus, n = 1)

#     cursor.close()
#     # connection.close()

#     bm25_output = ''.join(bm25_output)
#     return bm25_output


  
    

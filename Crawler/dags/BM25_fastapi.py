from Connection import getConnection
import global_variables as gv
import pandas as pd
import json
import pickle
from io import BytesIO
from BM25 import BM25Okapi

def export_bm25_model():
     minio = gv.get_minio_client()
     conn = getConnection()
     cursor = conn.cursor()

     cursor.execute("SELECT content FROM news")

     datacorpus = cursor.fetchall()

     df = pd.DataFrame(datacorpus, columns=['content'])
     corpus = df['content'].tolist()

     tokenized_corpus = [str(doc).split(" ") for doc in corpus]

     bm25 = BM25Okapi(tokenized_corpus)

     file = pickle.dumps(bm25)
     file_buffer = BytesIO(file)
          
     minio.put_object(gv.bucket_bm25,"bm25.pkl",file_buffer,len(file))

     cursor.close()
     getConnection().close()

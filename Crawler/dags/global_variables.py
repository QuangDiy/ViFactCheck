
# --------------- #
# PACKAGE IMPORTS #
# --------------- #
# import logging
# import os
from minio import Minio

# ----------------------- #
# Configuration variables #
# ----------------------- #

# Minio access
minio_endpoint = "localhost:9000"
minio_access_key="TzPEPI2j7edAHlnDdbEH"
minio_secret_key="RIEDGijyAxQ6RttR0EUtdg317IDzpTVVSxbK0HUN"
#Postgresql
#host.docker.internal
psql_host="localhost"
psql_port=5433
psql_database="vfc-news"
psql_user="admin"
psql_password="admin"
#Airflow Dataset


#Minio Bucket
bucket_baothanhnien ="baothanhnien"
bucket_baochinhphu ="baochinhphu"
bucket_vnexpress ="vnexpress"
bucket_bm25="bm25model"

def get_minio_client():
    client = Minio(minio_endpoint, minio_access_key, minio_secret_key, secure=False)
    return client


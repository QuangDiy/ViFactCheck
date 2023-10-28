# import include.global_variables as gv
import global_variables as gv
import psycopg2
import pandas as pd
from io import BytesIO


def getConnection():
    con = psycopg2.connect(
        host = gv.psql_host,
        port = gv.psql_port,
        user = gv.psql_user,
        password = gv.psql_password,
        database = gv.psql_database,
    )
    return con

def InsertData(df):
    # csv_string = df.to_csv(index=False)
    # csv_data = csv_string.encode()
    # conn = gv.get_minio_client()
    # try:
    #     conn.put_object(bucket_name,file_name,BytesIO(csv_data),len(csv_data))
    #     print(f"{file_name} CSV data uploaded successfully.")
    # except: 
    #     print(f"Error uploading {file_name} CSV data")

    conn = getConnection()
    conn.autocommit = True
    cur = conn.cursor()

    for _, row in df.iterrows():
        url = row['Link']
        title= row['Title']
        description = row['Mô tả']
        content = row['Nội dung']
        topic = row['Topic']
        news_type = row['News Type']
        date_publish = row['Ngày đăng']
        news_name = row['Tên báo']
        try:
            insert_query = "INSERT INTO news (url, title, description, content, topic, news_type, news_name, date_publish) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"  
            data = (url, title, description, content, topic, news_type, news_name, date_publish)
            cur.execute(insert_query, data)
            print(f"{url} insert success")
        except psycopg2.Error as e:
            print(e.pgerror)
            continue
    conn.commit()
    cur.close()
    conn.close()

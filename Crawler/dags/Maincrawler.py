from Baochinhphucrawler import BaoCP_df_to_DB
from Thanhniencrawler import Thanhnien_df_to_DB
from VnExpresscrawler import VNE_df_to_DB
from BM25_fastapi import export_bm25_model

def crawl():
    try:
        BaoCP_df_to_DB()
        print("Báo Chính Phủ success")
        Thanhnien_df_to_DB()
        print("Báo Thanh Niên success")
        VNE_df_to_DB()
        print("Báo VnExpress success")
        export_bm25_model()
        print("Model BM25 success")
    except:
        print("Errorrrrrrrrrrrr")
    

if __name__ =='__main__':
    crawl()
from bs4 import BeautifulSoup
import httpx
import pandas as pd
# from include.Connection import InsertData
# import include.global_variables as gv
from Connection import InsertData
import global_variables as gv
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')
topic =[]
title =[]
des =[]
content =[]
links=[]
tenbao=[]
date = []
link_temp =[]
news_type=[]
content_temp =""
tenbao='Báo Chính Phủ'
topiclist = {
"Chính trị": "https://baochinhphu.vn/chinh-tri.htm",
"Kinh tế": "https://baochinhphu.vn/kinh-te.htm",
"Văn hoá": "https://baochinhphu.vn/van-hoa.htm",
"Xã hội": "https://baochinhphu.vn/xa-hoi.htm",
"Khoa giáo":"https://baochinhphu.vn/khoa-giao.htm",
"Quốc tế":"https://baochinhphu.vn/quoc-te.htm"
}
filename = "Baochinhphu_"

def news_classifier(link):
  html = httpx.get(link,follow_redirects=True)
  soup = BeautifulSoup(html)
  if ("media" in link): #Video
    a =  soup.title.get_text()
    b = (soup.find(attrs={"name":"description"}).attrs)['content']
    c = None
    d = (soup.find(attrs={"property":"article:published_time"}).attrs)['content']
    e = "Text"
    return a,b,c,d,e
  else: #magazine
    a = soup.title.get_text()
    b = (soup.find(attrs={"name":"description"}).attrs)['content']
    content_temp =""
    for i in soup.find_all("p"):
      content_temp += i.get_text(" " ,strip=True)
    c = content_temp 
    d = (soup.find(attrs={"name": "distributionDate"}).attrs)['value']
    e = "Magazine"
    return a,b,c,d,e

def get_all_link(topiclist):
  for i in topiclist:
    print(topiclist[i])
    html = httpx.get(topiclist[i])
    soup = BeautifulSoup(html)
    for div in soup.find_all("div",class_="box-stream-item"):
      links.append("https://baochinhphu.vn" + f"{div.find('a').get('href')}")
      topic.append(i)
  print(len(links))

def parsing_link():
  for lk in links:
    with httpx.Client(timeout=40.0) as client:  # Set timeout to 30 seconds
      html = client.get(lk,follow_redirects=True)
    soup = BeautifulSoup(html)
    try:
      a=(soup.find("h1",class_="detail-title").get_text())
      b=(soup.find("h2", class_="detail-sapo").get_text(strip=True))
      c=(soup.find(attrs={"data-role": "content"}).get_text(" ", strip=True))
      d=(soup.find("div", class_="detail-time").get_text(" ", strip=True))
    except:
      try:
          a,b,c,d,e = news_classifier(lk)
          title.append(a)
          des.append(b)
          content.append(c)
          date.append(d)
          news_type.append(e)
      except:
          title.append(None)
          des.append(None)
          content.append(None)
          date.append(None)
          news_type.append(None)
    else: 
      title.append(a)
      des.append(b)
      content.append(c)
      date.append(d)
      news_type.append("Text")


def BaoCP_df_to_DB():
  get_all_link(topiclist)
  parsing_link()
  df = pd.DataFrame({ 'Title':title, 'Link':links, 'Topic':topic, 'Mô tả':des, "Nội dung":content,"Tên báo":tenbao, "Ngày đăng":date, "News Type":news_type}) #Tạo DF
  InsertData(df)
  
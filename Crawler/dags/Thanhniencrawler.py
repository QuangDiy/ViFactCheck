from bs4 import BeautifulSoup
import httpx
import pandas as pd
from datetime import datetime
import sys

from Connection import InsertData
import global_variables as gv

import warnings
warnings.filterwarnings('ignore')
topic =[]
title =[]
des =[]
content =[]
links=[]
tenbao=[]
date = []
news_type=[]
link_temp =[]
tenbao='Báo Thanh Niên'
topiclist = {
"Thời sự": "https://thanhnien.vn/thoi-su.htm",
"Thế giới": "https://thanhnien.vn/the-gioi.htm",
"Kinh tế":"https://thanhnien.vn/kinh-te.htm",
"Đời sống":"https://thanhnien.vn/doi-song.htm",
"Giải trí":"https://thanhnien.vn/giai-tri.htm",
"Thể thao":"https://thanhnien.vn/the-thao.htm",
"Giáo dục":"https://thanhnien.vn/giao-duc.htm",
"Sức khoẻ":"https://thanhnien.vn/suc-khoe.htm",
"Giới trẻ""":"https://thanhnien.vn/gioi-tre.htm",
"Du lịch":"https://thanhnien.vn/du-lich.htm",
"Văn hoá":"https://thanhnien.vn/van-hoa.htm",
"Công nghệ - Game":"https://thanhnien.vn/cong-nghe-game.htm",
"Xe":"https://thanhnien.vn/xe.htm",
"Tiêu dùng":"https://thanhnien.vn/tieu-dung-thong-minh.htm"
}

def news_classifier(link):
  html = httpx.get(link,follow_redirects=True)
  soup = BeautifulSoup(html)
  if ("video" in link): #Video
    a = (soup.find("h1",class_="title").get_text())
    b = (soup.find("div",class_="lead_detail").get_text(" ",strip=True))
    c = None
    d = (soup.find("span", class_="time").get_text())
    e = "Video"
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
    for div in soup.find_all("h3" , class_="box-title-text"):
      links.append("https://thanhnien.vn" + f"{div.find('a').get('href')}")
      topic.append(i)
  print(len(links))

def parsing_link():
  content_temp=""
  for lk in links:
    content_temp=""
    with httpx.Client(timeout=40.0) as client:  # Set timeout to 30 seconds
      html = client.get(lk,follow_redirects=True)
    soup = BeautifulSoup(html)
    try:
      a= soup.title.get_text()
      b = (soup.find(attrs={"name":"description"}).attrs)['content']
      for i in soup.find_all("p"):
        content_temp = content_temp + i.get_text(" ",strip=True) 
      c = content_temp.replace('Bình luận ( 0 )Hotline0906 645 777Liên hệ quảng cáo0908 780 404Tổng biên tập: Nguyễn Ngọc ToànPhó tổng biên tập: Hải ThànhPhó tổng biên tập: Lâm Hiếu DũngỦy viên Ban biên tập - Tổng Thư ký tòa soạn: Trần Việt HưngBình luận ( 0 )',"")
      d=(soup.find(attrs={"data-role": "publishdate"}).get_text(" ", strip=True))
      e="Text"
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
      news_type.append(e)


def Thanhnien_df_to_DB():
  get_all_link(topiclist)
  parsing_link()
  df = pd.DataFrame({ 'Title':title, 'Link':links, 'Topic':topic, 'Mô tả':des, "Nội dung":content,"Tên báo":tenbao, "Ngày đăng":date, "News Type":news_type}) #Tạo DF
  InsertData(df)

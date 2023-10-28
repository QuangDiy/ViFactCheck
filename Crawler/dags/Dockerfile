FROM python:3.10-slim

WORKDIR /Users/tth/airflow/crawler
ENV network host
COPY . .

RUN pip install -r requirements_crawler.txt
#CMD ["python","Maincrawler.py"]
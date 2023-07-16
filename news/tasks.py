from core.celery import app
import requests
from typing import Tuple
from news import query as news_query
from django.conf import settings

@app.task
def some_tasks():
    print("Execute me every minute please !!!")

@app.task
def get_stock_news(url,headers,category_name) -> Tuple[int,dict]:
    try:
        response = requests.get(url,headers = headers)
        if response.status_code == 200:
            print(response.json())
            news_query.NewsHandler.create_stock_news(response.json(),category_name)
        else:
            print(response.json())
            return 400,response.json()
    except Exception as e:
        return 400,str(e)

from core.celery import app
import requests
from typing import Tuple
from news import query as news_query

@app.task
def some_tasks():
    print("Execute me every minute please !!!")

@app.task
def get_news(url: str,headers,category_name,queryString: dict=None) -> Tuple[int,dict]:
    try:
        response = requests.get(url,headers = headers,params=queryString)
        if response.status_code == 200:
            news_query.NewsHandler.create_news(response.json(),category_name)
        else:
            return 400,response.json()
    except Exception as e:
        return 400,str(e)
    

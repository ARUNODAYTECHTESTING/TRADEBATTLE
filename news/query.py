from news import models as news_models
import pdb

class CategoryHandler:
    @classmethod
    def get_category_by_name(cls,category_name):
        return news_models.Category.objects.filter(name__icontains = category_name).first()

class NewsHandler:
    @classmethod
    def is_category_has_news(cls,category):
        if category.news.filter().count() > 0:
           return True
       
        return False
        
    @classmethod
    def create_news(cls, news: list,category_name):
        try:
            if category_name in ["technology","business","international"]:
                news = news["articles"]

            category = CategoryHandler.get_category_by_name(category_name=category_name)
            if not NewsHandler.is_category_has_news(category):
                news_models.News.objects.create(news=news,category=category)
            else:
                news_models.News.objects.filter(category = category).update(news=news,category=category)
        except Exception as e:
            print("Error", e)
            

  
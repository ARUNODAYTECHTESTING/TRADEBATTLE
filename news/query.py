from news import models as news_models
import pdb

class CategoryHandler:
    @classmethod
    def get_category_by_name(cls,category_name):
        return news_models.Category.objects.filter(name__icontains = category_name).first()

class NewsHandler:

    @classmethod
    def create_news(cls, news: list,category_name):
        try:
            if category_name in ["technology","business","international"]:
                news = news["articles"]
            category = CategoryHandler.get_category_by_name(category_name=category_name)
            news_models.News.objects.create(news=news,category=category)
        except Exception as e:
            print("Error", e)
            

  
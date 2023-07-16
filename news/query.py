from news import models as news_models
import pdb
class CategoryHandler:
    @classmethod
    def get_category_by_name(cls,category_name):
        return news_models.NewsCategory.objects.filter(name__icontains = category_name).first()

class NewsHandler:

    @classmethod
    def create_stock_news(cls, news: list,category_name):
        category = CategoryHandler.get_category_by_name(category_name=category_name)
        news_models.News.objects.create(stock_news=news,category=category)

  
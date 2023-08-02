from django.contrib import admin
from .models import (
    Question,
    Answer,
    Battle,
    RankCard,
    StockVariant,
    Stock,
    StockCategory,
    BattleType
)

# Register your models here.

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Battle)
admin.site.register(RankCard)
admin.site.register(StockVariant)
admin.site.register(Stock)
admin.site.register(StockCategory)
admin.site.register(BattleType)

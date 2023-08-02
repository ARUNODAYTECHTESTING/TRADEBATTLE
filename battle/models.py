from django.db import models
from ckeditor.fields import RichTextField


# Create your models here.


class BattleType(models.Model):
    name = models.CharField(unique=True, max_length=256)

    def __str__(self) -> str:
        return self.name


class StockVariant(models.Model):
    name = models.CharField(unique=True, max_length=256)

    def __str__(self) -> str:
        return self.name


class ContestType(models.Model):
    name = models.CharField(unique=True, max_length=256)


class Battle(models.Model):
    contest_type = models.ForeignKey(
        ContestType, on_delete=models.CASCADE, db_index=True
    )
    stocks_type = models.ForeignKey(
        StockVariant, on_delete=models.CASCADE, db_index=True
    )
    battle_type = models.ForeignKey(BattleType, on_delete=models.CASCADE, db_index=True)
    start_time = models.DateTimeField(db_index=True)
    end_time = models.DateTimeField()
    entry_amount = models.IntegerField()
    user_spot = models.IntegerField()
    total_spot = models.IntegerField()
    winner = models.IntegerField()
    payout_done = models.BooleanField(default=False)
    pool_size = models.IntegerField()
    filled = models.BooleanField()


class RankCard(models.Model):
    battle = models.ForeignKey(Battle, on_delete=models.CASCADE, db_index=True)
    lower = models.IntegerField()
    upper = models.IntegerField(null=True)
    amount = models.IntegerField()


class Question(models.Model):
    battle = models.ForeignKey(Battle, on_delete=models.CASCADE, db_index=True)
    text = RichTextField()
    points = models.IntegerField()


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, db_index=True)
    text = RichTextField()
    correct = models.BooleanField(default=False)


class BattleEnrolment(models.Model):
    user = models.ForeignKey(
        "authentication.User", on_delete=models.CASCADE, db_index=True
    )
    battle = models.ForeignKey(Battle, on_delete=models.CASCADE, db_index=True)
    points = models.IntegerField()
    rank = models.IntegerField()
    winning = models.IntegerField()
    # transaction_id = models.ForeignKey()


class BattleEnrolmentBid(models.Model):
    enrollment = models.ForeignKey(BattleEnrolment, on_delete=models.CASCADE)
    option = models.ForeignKey(Answer, on_delete=models.CASCADE)
    first_multiplier = models.BooleanField(default=False)
    second_multiplier = models.BooleanField(default=False)


class StockCategory(models.Model):
    name = models.CharField(unique=True, max_length=256)

    def __str__(self) -> str:
        return self.name


class Stock(models.Model):
    MOVEMENT = ((1, "Up"), (2, "Down"))
    name = models.CharField(unique=True, max_length=250)
    category = models.ForeignKey(StockCategory, on_delete=models.DO_NOTHING, null=True, blank=True)
    variant = models.ForeignKey(StockVariant, on_delete=models.DO_NOTHING)
    image = models.ImageField(upload_to="stock_image", default="stock_image/defaut.png")
    current_price = models.IntegerField(default=0)
    movement = models.PositiveSmallIntegerField(choices=MOVEMENT)
    move = models.FloatField(default=0.0)
    

    def __str__(self) -> str:
        return self.name

class LeagueBattleBid(models.Model):
    enrollment = models.ForeignKey(BattleEnrolment, on_delete=models.CASCADE)
    user = models.ForeignKey("authentication.User", on_delete=models.CASCADE, db_index=True)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    multiplier = models.BooleanField(default=False)

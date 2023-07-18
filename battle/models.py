from django.db import models
from ckeditor.fields import RichTextField


# Create your models here.


class Battle(models.Model):

    BATTLE_TYPE = (
        (1, "Predict Battle"),
        (2, "Time Battle"),
        (3, "League Battle"),
        (4, "Solo Battle")
    )

    STOCK_VARIANT = (
        (1, "Indian Stock"),
        (2, "US Stock"),
        (3, "Crypto")
    )

    CONTEST_TYPE = (
        (1, "Head To Head"),
        (2, "Practi")
    )
    contest_type = models.PositiveSmallIntegerField(choices=CONTEST_TYPE, db_index=True)
    stocks_type = models.PositiveSmallIntegerField(choices=STOCK_VARIANT, db_index=True)
    battle_type = models.PositiveSmallIntegerField(choices=BATTLE_TYPE, db_index=True)
    start_time = models.DateTimeField(db_index=True)
    end_time = models.DateTimeField()
    entry_amount = models.IntegerField()
    user_spot = models.IntegerField()
    total_spot = models.IntegerField()
    winner = models.IntegerField()
    payout_done = models.BooleanField(default=False)
    pool_size = models.IntegerField()


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
    text =  RichTextField()
    correct = models.BooleanField(default=False)


class BattleEnrolment(models.Model):
    user = models.ForeignKey("authentication.User", on_delete=models.CASCADE, db_index= True)
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


    
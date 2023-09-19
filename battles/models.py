# models.py
from avtar import models as avtar_models
from django.db import models

BATTLE_STATUS_CHOICES = (
    ('live', 'Live'),
    ('upcoming', 'Upcoming'),
    ('completed', 'Completed'),
)

class MarketType(avtar_models.TmeStampModel):
    name = models.CharField(max_length=255)
    max_entries = models.IntegerField()
    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return self.name


class BattleCategory(avtar_models.TmeStampModel):
    name = models.CharField(max_length=255)
    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return self.name


class TimeBattle(avtar_models.TmeStampModel):
    name = models.CharField(max_length=255)
    market_type = models.ForeignKey(MarketType, on_delete=models.CASCADE)
    category = models.ForeignKey(BattleCategory, on_delete=models.CASCADE)
    battle_image = models.ImageField(upload_to='TimeBattle',default="battles/defaut.png")
    enrollment_start_time = models.DateTimeField()
    enrollment_end_time = models.DateTimeField()
    battle_start_time = models.DateTimeField()
    battle_end_time = models.DateTimeField()
    status = models.CharField(
        max_length=10, choices=BATTLE_STATUS_CHOICES,default='upcoming'
    )
    battle_recurrent_count = models.IntegerField()
    battle_frequency = models.CharField(max_length=255)
    trivia = models.TextField()
    coins_multiplier_constant = models.FloatField()
    experience_points_multiplier_constant = models.FloatField()
    max_winnings = models.FloatField()
    max_participants = models.PositiveIntegerField(default=0)
    entry_fee = models.FloatField()
    questions_set = models.ForeignKey('QuestionSet',on_delete=models.CASCADE)
    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return self.name


class TimeBattleUser(avtar_models.TmeStampModel):
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE,db_index=True,related_name='time_battle_users')
    battle_id = models.ForeignKey(TimeBattle, on_delete=models.CASCADE)
    submitted_time_and_answers = models.JSONField()
    total_answer_duration = models.FloatField()
    enrollment_time = models.DateTimeField()
    status = models.CharField(max_length=255)
    coins_earned = models.FloatField()
    experience_points_earned = models.CharField(max_length=250)
    entry_fees_paid = models.CharField(max_length=250)
    questions_set = models.ForeignKey('QuestionSet',on_delete=models.CASCADE)
    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return self.user



class SoloBattle(avtar_models.TmeStampModel):
    name = models.CharField(max_length=255)
    market_type = models.ForeignKey(MarketType, on_delete=models.CASCADE)
    category = models.ForeignKey(BattleCategory, on_delete=models.CASCADE)
    battle_image = models.ImageField(upload_to='SoloBattle',default="battles/defaut.png")
    enrollment_start_time = models.DateTimeField()
    enrollment_end_time = models.DateTimeField()
    battle_start_time = models.DateTimeField()
    battle_end_time = models.DateTimeField()
    status = models.CharField(
        max_length=10, choices=BATTLE_STATUS_CHOICES,default='upcoming'
    )
    battle_recurrent_count = models.IntegerField()
    battle_frequency = models.CharField(max_length=255)
    trivia = models.TextField()
    coins_multiplier_constant = models.FloatField()
    experience_points_multiplier_constant = models.FloatField()
    max_winnings = models.FloatField()
    max_participants = models.PositiveIntegerField(default=0)
    entry_fee = models.FloatField()
    max_allowed_stocks = models.IntegerField()
    multiplier_options = models.JSONField()
    questions_set = models.ForeignKey('QuestionSet',on_delete=models.CASCADE)
    max_entries = models.IntegerField()
    
    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return self.name

class SoloBattleUser(avtar_models.TmeStampModel):
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE,db_index=True,related_name='solo_battle_users')
    battle = models.ForeignKey(SoloBattle, on_delete=models.CASCADE)
    number_of_entries = models.IntegerField()
    submitted_time_and_answers = models.JSONField()
    enrollment_time = models.DateTimeField()
    status = models.CharField(max_length=255)
    coins_earned = models.FloatField()
    experience_points_earned = models.CharField(max_length=250)
    entry_fees_paid = models.CharField(max_length=250)
    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return self.user



class LeagueBattle(avtar_models.TmeStampModel):
    name = models.CharField(max_length=255)
    market_type = models.ForeignKey(MarketType, on_delete=models.CASCADE)
    category = models.ForeignKey(BattleCategory, on_delete=models.CASCADE)
    battle_image = models.ImageField(upload_to='LeagueBattle',default="battles/defaut.png")
    enrollment_start_time = models.DateTimeField()
    enrollment_end_time = models.DateTimeField()
    battle_start_time = models.DateTimeField()
    battle_end_time = models.DateTimeField()
    status = models.CharField(
        max_length=10, choices=BATTLE_STATUS_CHOICES,default='upcoming'
    )
    battle_recurrent_count = models.IntegerField()
    battle_frequency = models.CharField(max_length=255)
    trivia = models.TextField()
    coins_multiplier_constant = models.FloatField()
    experience_points_multiplier_constant = models.FloatField()
    max_winnings = models.FloatField()
    max_participants = models.PositiveIntegerField(default=0)
    entry_fee = models.FloatField()
    max_allowed_stocks = models.IntegerField()
    multiplier_options = models.JSONField()
    max_entries = models.IntegerField()
    
    
    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return self.name

class LeagueBattleUser(avtar_models.TmeStampModel):
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE,db_index=True,related_name='league_battle_users')
    battle = models.ForeignKey(LeagueBattle, on_delete=models.CASCADE)
    number_of_entries = models.IntegerField()
    submitted_time_and_answers = models.JSONField()
    enrollment_time = models.DateTimeField()
    total_answer_duration = models.FloatField()
    coins_earned = models.FloatField()
    status = models.CharField(max_length=255)
    experience_points_earned = models.CharField(max_length=250)
    entry_fees_paid = models.CharField(max_length=250)
    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return self.user

class PredictBattle(avtar_models.TmeStampModel):
    name = models.CharField(max_length=255)
    market_type = models.ForeignKey(MarketType, on_delete=models.CASCADE)
    category = models.ForeignKey(BattleCategory, on_delete=models.CASCADE)
    battle_image = models.ImageField(upload_to='PredictBattle',default="battles/defaut.png")
    enrollment_start_time = models.DateTimeField()
    enrollment_end_time = models.DateTimeField()
    battle_start_time = models.DateTimeField()
    battle_end_time = models.DateTimeField()
    status = models.CharField(
        max_length=10, choices=BATTLE_STATUS_CHOICES,default='upcoming'
    )
    battle_recurrent_count = models.IntegerField()
    battle_frequency = models.CharField(max_length=255)
    trivia = models.TextField()
    coins_multiplier_constant = models.FloatField()
    experience_points_multiplier_constant = models.FloatField()
    max_winnings = models.FloatField()
    max_participants = models.PositiveIntegerField(default=0)
    entry_fee = models.FloatField()
    max_allowed_stocks = models.IntegerField()
    multiplier_options = models.JSONField()
    max_entries = models.IntegerField()
    questions_set = models.ForeignKey('QuestionSet',on_delete=models.CASCADE)
    
    
    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return self.name

class PredictBattleUser(avtar_models.TmeStampModel):
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE,db_index=True,related_name='pred_battle_users')
    battle = models.ForeignKey(PredictBattle, on_delete=models.CASCADE)
    number_of_entries = models.IntegerField()
    submitted_time_and_answers = models.JSONField()
    enrollment_time = models.DateTimeField()
    total_answer_duration = models.FloatField()
    coins_earned = models.FloatField()
    status = models.CharField(max_length=255)
    experience_points_earned = models.CharField(max_length=250)
    entry_fees_paid = models.CharField(max_length=250)
    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return self.user

class QuestionSet(avtar_models.TmeStampModel):
    name = models.CharField(max_length=255)
    questions = models.JSONField()
    answer = models.ManyToManyField('Answers')
    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return self.name

class Answers(avtar_models.TmeStampModel):
    option = models.CharField(max_length=150)
    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return self.option

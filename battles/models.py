# models.py
from django.utils import timezone
from authentication import models as auth_models
from django.db import models
from django.contrib.postgres.fields import ArrayField

BATTLE_STATUS_CHOICES = (
    ('live', 'Live'),
    ('upcoming', 'Upcoming'),
    ('completed', 'Completed'),
    ('expired', 'Expired')
)

class MarketType(auth_models.TmeStampModel):
    name = models.CharField(max_length=255)
    max_entries = models.IntegerField()
    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return self.name


class BattleCategory(auth_models.TmeStampModel):
    name = models.CharField(max_length=255)
    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return self.name


class TimeBattle(auth_models.TmeStampModel):
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

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return self.name


class TimeBattleUser(auth_models.TmeStampModel):
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE,db_index=True,related_name='time_battle_users')
    battle_id = models.ForeignKey(TimeBattle, on_delete=models.CASCADE)
    submitted_time_and_answers = models.JSONField()
    total_answer_duration = models.FloatField()
    enrollment_time = models.DateTimeField()
    status = models.CharField(max_length=255)
    coins_earned = models.FloatField()
    experience_points_earned = models.CharField(max_length=250)
    entry_fees_paid = models.CharField(max_length=250)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return self.user



class SoloBattle(auth_models.TmeStampModel):
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
    completed_battle_count = models.PositiveBigIntegerField(default=0)
    trivia = models.TextField()
    coins_multiplier_constant = models.FloatField()
    experience_points_multiplier_constant = models.FloatField()
    max_winnings = models.FloatField()
    max_participants = models.PositiveIntegerField(default=0)
    entry_fee = models.FloatField()
    max_allowed_stocks = models.IntegerField()
    multiplier_options = models.JSONField()
    questions_set = ArrayField(models.PositiveIntegerField(),null=True, blank=True)
    max_entries = models.IntegerField()
    
    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return self.name

class SoloBattleUser(auth_models.TmeStampModel):
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
        return self.battle



class LeagueBattle(auth_models.TmeStampModel):
    name = models.CharField(max_length=255)
    market_type = models.ForeignKey(MarketType, on_delete=models.CASCADE)
    category = models.ForeignKey(BattleCategory, on_delete=models.CASCADE)
    battle_image = models.ImageField(upload_to='LeagueBattle',default="battles/defaut.png")
    enrollment_start_time = models.DateTimeField() #timezone
    enrollment_end_time = models.DateTimeField(verbose_name='Enrollment End Time',help_text='Format: dd-mm-yyyy HH:MM:SS (24-hour)')
    battle_start_time = models.DateTimeField()
    battle_end_time = models.DateTimeField()
    status = models.CharField(
        max_length=10, choices=BATTLE_STATUS_CHOICES,default='upcoming'
    )
    battle_recurrent_count = models.IntegerField()
    battle_frequency = models.CharField(max_length=255)
    trivia = models.TextField(blank=True,null=True) #optional
    coins_multiplier_constant = models.FloatField()
    experience_points_multiplier_constant = models.FloatField()
    max_winnings = models.FloatField() #integer
    max_participants = models.PositiveIntegerField(default=0)
    entry_fee = models.FloatField()
    max_allowed_stocks = models.IntegerField()
    multiplier_options = models.JSONField()
    max_entries = models.IntegerField()
    number_of_winners = models.IntegerField(null=True,blank=True)
    #completed battle count (how many times it ran)
    completed_battle_count = models.IntegerField(default=0,blank=True,null=True)
    
    def __str__(self) -> str:
        return self.name

class LeagueBattleUser(auth_models.TmeStampModel):
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE,db_index=True,related_name='league_battle_users')
    battle = models.ForeignKey(LeagueBattle, on_delete=models.CASCADE)
    number_of_entries = models.IntegerField()
    submitted_time_and_answers = models.JSONField()
    enrollment_time = models.DateTimeField()
    total_answer_duration = models.FloatField()
    coins_earned = models.FloatField()
    status = models.CharField(max_length=255) #choice_field
    experience_points_earned = models.CharField(max_length=250)
    entry_fees_paid = models.CharField(max_length=250)
    class Meta:
        ordering = ("-created_at",)
        
    # def __str__(self) -> str:
    #     return self.user


class PredictBattle(auth_models.TmeStampModel):
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

    
    
    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return self.name

class PredictBattleUser(auth_models.TmeStampModel):
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


# TODO: Question tables
class QuestionsBase(auth_models.TmeStampModel):
    name = models.CharField(max_length=64)
    options = models.JSONField()
    correct_answer = models.CharField(max_length=124)


    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.name

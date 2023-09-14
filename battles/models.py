# models.py

from django.db import models


class MarketType(models.Model):
    name = models.CharField(max_length=255)
    max_entries = models.IntegerField()


class BattleCategory(models.Model):
    name = models.CharField(max_length=255)


class TimeBattle(models.Model):
    name = models.CharField(max_length=255)
    market_type = models.ForeignKey(MarketType, on_delete=models.CASCADE)
    category = models.ForeignKey(BattleCategory, on_delete=models.CASCADE)
    battle_image = models.ImageField(upload_to='TimeBattle',default="battles/defaut.png")
    enrollment_start_time = models.DateTimeField()
    enrollment_end_time = models.DateTimeField()
    battle_start_time = models.DateTimeField()
    battle_end_time = models.DateTimeField()
    status = models.CharField(max_length=255)
    battle_recurrent_count = models.IntegerField()
    battle_frequency = models.CharField(max_length=255)
    trivia = models.TextField()
    coins_multiplier_constant = models.FloatField()
    experience_points_multiplier_constant = models.FloatField()
    max_winnings = models.FloatField()
    max_participants = models.IntegerField()
    entry_fee = models.FloatField()
    questions_set = models.ManyToManyField('QuestionSet')


class TimeBattleUser(models.Model):
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE)
    battle = models.ForeignKey(TimeBattle, on_delete=models.CASCADE)
    number_of_entries = models.IntegerField()
    submitted_time_and_answers = models.JSONField()
    enrollment_time = models.DateTimeField()
    total_answer_duration = models.FloatField()
    coins_earned = models.FloatField()
    status = models.CharField(max_length=255)



class SoloBattle(models.Model):
    name = models.CharField(max_length=255)
    market_type = models.ForeignKey(MarketType, on_delete=models.CASCADE)
    category = models.ForeignKey(BattleCategory, on_delete=models.CASCADE)
    battle_image = models.ImageField(upload_to='SoloBattle',default="battles/defaut.png")
    enrollment_start_time = models.DateTimeField()
    enrollment_end_time = models.DateTimeField()
    battle_start_time = models.DateTimeField()
    battle_end_time = models.DateTimeField()
    status = models.CharField(max_length=255)
    battle_recurrent_count = models.IntegerField()
    battle_frequency = models.CharField(max_length=255)
    trivia = models.TextField()
    coins_multiplier_constant = models.FloatField()
    experience_points_multiplier_constant = models.FloatField()
    max_winnings = models.FloatField()
    max_participants = models.IntegerField()
    entry_fee = models.FloatField()
    questions_set = models.ManyToManyField('QuestionSet')

class SoloBattleUser(models.Model):
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE)
    battle = models.ForeignKey(SoloBattle, on_delete=models.CASCADE)
    number_of_entries = models.IntegerField()
    submitted_time_and_answers = models.JSONField()
    enrollment_time = models.DateTimeField()
    total_answer_duration = models.FloatField()
    coins_earned = models.FloatField()
    status = models.CharField(max_length=255)



class LeagueBattle(models.Model):
    name = models.CharField(max_length=255)
    market_type = models.ForeignKey(MarketType, on_delete=models.CASCADE)
    category = models.ForeignKey(BattleCategory, on_delete=models.CASCADE)
    battle_image = models.ImageField(upload_to='LeagueBattle',default="battles/defaut.png")
    enrollment_start_time = models.DateTimeField()
    enrollment_end_time = models.DateTimeField()
    battle_start_time = models.DateTimeField()
    battle_end_time = models.DateTimeField()
    status = models.CharField(max_length=255)
    battle_recurrent_count = models.IntegerField()
    battle_frequency = models.CharField(max_length=255)
    trivia = models.TextField()
    coins_multiplier_constant = models.FloatField()
    experience_points_multiplier_constant = models.FloatField()
    max_winnings = models.FloatField()
    max_participants = models.IntegerField()
    entry_fee = models.FloatField()
    questions_set = models.ManyToManyField('QuestionSet')

class LeagueBattleUser(models.Model):
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE)
    battle = models.ForeignKey(LeagueBattle, on_delete=models.CASCADE)
    number_of_entries = models.IntegerField()
    submitted_time_and_answers = models.JSONField()
    enrollment_time = models.DateTimeField()
    total_answer_duration = models.FloatField()
    coins_earned = models.FloatField()
    status = models.CharField(max_length=255)


class QuestionSet(models.Model):
    name = models.CharField(max_length=255)
    questions = models.JSONField()
    answer = models.ManyToManyField('Answers')

class Answers(models.Model):
    option = models.CharField(max_length=150)

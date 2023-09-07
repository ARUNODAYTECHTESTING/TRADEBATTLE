from django.db import models
from avtar import models as avtar_models
BATTLE_STATUS_CHOICES = (
    ('live', 'Live'),
    ('upcoming', 'Upcoming'),
    ('completed', 'Completed'),
)

class MasterBattle(avtar_models.TmeStampModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
   
    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return self.name


class Battle(avtar_models.TmeStampModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    battle_type = models.ForeignKey(MasterBattle, on_delete=models.CASCADE, db_index=True,related_name='battle')
    battle_status = models.CharField(
        max_length=10, choices=BATTLE_STATUS_CHOICES,default='upcoming'
    )
   
    icon = models.ImageField(upload_to='battles')
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    price = models.PositiveBigIntegerField()
    # TODO: added player joins and entry fees
    player_joined = models.PositiveIntegerField(default=0)
    entry_fee = models.FloatField(default=0.0)


    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return self.name


class QuestionType(avtar_models.TmeStampModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return self.name


class Question(avtar_models.TmeStampModel):
    id = models.AutoField(primary_key=True)
    battle = models.ForeignKey(Battle, on_delete=models.CASCADE,related_name='questions')
    question_type = models.ForeignKey(QuestionType, on_delete=models.CASCADE,related_name='questions')
    name = models.CharField(max_length=255)
   
    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return self.name
    


class Option(avtar_models.TmeStampModel):
    id = models.AutoField(primary_key=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE,related_name='options')
    name = models.CharField(max_length=255)
  
    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return self.name


class QuestionAttempt(avtar_models.TmeStampModel):
    id = models.AutoField(primary_key=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE,related_name='question_attempts')
    option = models.ForeignKey(Option, on_delete=models.CASCADE,related_name='question_attempts')
    user = user = models.ForeignKey(
        "authentication.User", on_delete=models.CASCADE, db_index=True,related_name='question_attempts'
    )
    total_number_of_entry = models.IntegerField()
    attempt = models.IntegerField()

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return f"{self.question.name} -> {self.option.name}"

class Answer(avtar_models.TmeStampModel):
    id = models.AutoField(primary_key=True)
    user = user = models.ForeignKey(
        "authentication.User", on_delete=models.CASCADE, db_index=True,related_name="answers"
    )
    option = models.ForeignKey(Option, on_delete=models.CASCADE,related_name="answers")

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return f"{self.user.email} -> {self.option.name}"
    
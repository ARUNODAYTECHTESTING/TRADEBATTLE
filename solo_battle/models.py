from django.db import models

BATTLE_STATUS_CHOICES = (
    ('live', 'Live'),
    ('upcoming', 'Upcoming'),
    ('completed', 'Completed'),
)

class MasterBattle(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.name


class Battle(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    battle_type = models.ForeignKey(MasterBattle, on_delete=models.CASCADE, db_index=True)
    battle_status = models.CharField(
        max_length=10, choices=BATTLE_STATUS_CHOICES
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    icon = models.ImageField(upload_to='battles')
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    price = models.IntegerField()
    
    def __str__(self) -> str:
        return self.name


class QuestionType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    def __str__(self) -> str:
        return self.name


class Question(models.Model):
    id = models.AutoField(primary_key=True)
    battle = models.ForeignKey(Battle, on_delete=models.CASCADE)
    question_type = models.ForeignKey(QuestionType, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self) -> str:
        return self.name
    


class Option(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self) -> str:
        return self.name


class QuestionAttempt(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
    user = user = models.ForeignKey(
        "authentication.User", on_delete=models.CASCADE, db_index=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_number_of_entry = models.IntegerField()
    attempt = models.IntegerField()


class Answer(models.Model):
    id = models.AutoField(primary_key=True)
    user = user = models.ForeignKey(
        "authentication.User", on_delete=models.CASCADE, db_index=True
    )
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
    
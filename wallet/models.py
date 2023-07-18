from django.db import models
import uuid

# Create your models here.

class Referal(models.Model):
    referer = models.ForeignKey(
        "authentication.User", on_delete=models.SET_NULL, null=True, related_name="referer"
    )
    user = models.ForeignKey(
        "authentication.User", on_delete=models.DO_NOTHING, related_name="user"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("referer", "user")


class Wallet(models.Model):
    user = models.OneToOneField("authentication.User", on_delete=models.CASCADE)
    deposit_bal = models.FloatField(default=0.0)
    bonus_bal = models.FloatField(default=0.0)
    winning_amount = models.FloatField(default=0.0)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.user.mobile
    

class Transaction(models.Model):
    AMOUNT_ACTION = (
        (1, "Credit"),
        (2, "Debit"),
    )
    CREDIT_TYPE = (
        (1, "Deposit"),
        (2, "Withdraw"),
        (3, "Bonus"),
        (4, "Winning"),
        (5, "Contest"),
        (6, "Refund"),
    )
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    amount = models.FloatField()
    message = models.TextField(blank=True)
    transaction_id = models.CharField(max_length=50, unique=True)
    action = models.IntegerField(choices=AMOUNT_ACTION)
    credit_type = models.IntegerField(choices=CREDIT_TYPE)
    created_at = models.DateTimeField(auto_now_add=True)
    tds = models.FloatField(null=True, blank=True)
    meta_data = models.JSONField(null=True)

    def save(self, *args, **kwargs):
        self.transaction_id = str(uuid.uuid4())[:18]
        if self.action == 1:
            if self.credit_type == 4:
                self.wallet.winning_amount += self.amount
            elif self.credit_type == 1:
                self.wallet.deposit_bal += self.amount
            elif self.credit_type == 3:
                self.wallet.bonus_bal += self.amount
        if self.action == 2 and self.credit_type == 2:
            self.wallet.winning_amount -= self.amount
        self.wallet.save()
        super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return f"{self.wallet.user.mobile} {self.amount}"

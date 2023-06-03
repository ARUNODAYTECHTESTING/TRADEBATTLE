from django.db import models

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

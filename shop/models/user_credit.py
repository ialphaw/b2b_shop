from django.db import models


class UserCredit(models.Model):
    """User credit model."""

    user = models.OneToOneField("auth.User", on_delete=models.CASCADE)
    credit = models.FloatField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.credit}"

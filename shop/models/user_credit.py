from django.db import models


class UserCredit(models.Model):
    """User credit model."""

    user = models.OneToOneField("auth.User", on_delete=models.CASCADE)
    credit = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.user.username} - {self.credit}"

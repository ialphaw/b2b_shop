from django.db import models

from shop.models import Transaction


class UserCredit(models.Model):
    """User credit model."""

    user = models.OneToOneField("auth.User", on_delete=models.CASCADE)
    credit = models.FloatField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.credit}"

    def make_transaction(self, category):
        """Create a transaction for the user credit."""
        
        Transaction.objects.create(
            user=self.user,
            amount=self.credit,
            category=category,
        )

    def save(self, *args, **kwargs):
        """Save the user credit and create a transaction if the credit has changed."""

        if not self.pk:
            self.make_transaction("i")
        else:
            original_user_credit = UserCredit.objects.get(pk=self.pk)
            if original_user_credit.credit != self.credit:
                if original_user_credit.credit < self.credit:
                    self.make_transaction("i")
                else:
                    self.make_transaction("d")

        super().save(*args, **kwargs)

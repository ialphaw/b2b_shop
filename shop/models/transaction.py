from django.db import models, transaction
from django.core.exceptions import ValidationError

from shop.models import UserCredit


class Transaction(models.Model):
    """Transaction model."""

    INCREASE = "i"
    DECREASE = "d"

    CATEGORY_CHOICES = (
        (INCREASE, "Increase"),
        (DECREASE, "Decrease"),
    )

    category = models.CharField(choices=CATEGORY_CHOICES, max_length=50)
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def get_category_display(self):
        """Return the category display name."""

        return dict(self.CATEGORY_CHOICES)[self.category]

    def __str__(self):
        return f"{self.user} - {self.amount} - {self.get_category_display()}"

    def save(self, *args, **kwargs):
        user_credit = UserCredit.objects.get(user=self.user)

        if self.category == "d":
            if user_credit.credit < self.amount:
                raise ValidationError(
                    "You do not have the required credit",
                    code="invalid",
                )

            user_credit.credit -= self.amount
        else:
            user_credit.credit += self.amount

        user_credit.save(update_fields=["credit"])

        super().save(*args, **kwargs)

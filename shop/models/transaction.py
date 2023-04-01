from django.db import models


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
    amount = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    def get_category_display(self):
        """Return the category display name."""
        
        return dict(self.CATEGORY_CHOICES)[self.category]

    def __str__(self):
        return f"{self.user} - {self.amount} - {self.get_category_display()}"

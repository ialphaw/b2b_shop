from django.db import models


class Transaction(models.Model):
    """Transaction model."""
    
    INCREASE = "i"
    DECREASE = "d"

    category = models.CharField(
        choices=((INCREASE, "Increase"), (DECREASE, "Decrease")), max_length=50
    )
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    amount = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.amount} - {self.category}"

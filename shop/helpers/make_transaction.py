from shop.models import Transaction


def make_transaction(category, amount, user):
    """Create a transaction for the user credit."""

    Transaction.objects.create(
        user=user,
        amount=amount,
        category=category,
    )

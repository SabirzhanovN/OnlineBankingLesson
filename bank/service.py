from django.db import transaction
from .models import Transfer


def make_transfer(from_account, to_account, amount):
    if from_account.balance < amount:
        raise (ValueError("Not enough money!"))
    if from_account == to_account:
        raise (ValueError("Choose another account"))

    with transaction.atomic():
        from_balance = from_account.balance - amount
        from_account.balance = from_balance
        from_account.save()

        to_balance = to_account.balance + amount
        to_account.balance = to_balance
        to_account.save()

        transfer = Transfer.objects.create(
            from_account=from_account,
            to_account=to_account,
            amount=amount
        )

    return transfer

from django.conf import settings
from django.db import models


class Customer(models.Model):
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    house = models.CharField(max_length=255)

    image = models.ImageField(null=True, upload_to="customerImages")

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.fname} {self.lname}"


class Account(models.Model):
    balance = models.DecimalField(
        default=0,
        max_digits=11,
        decimal_places=2
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT
    )

    def __str__(self):
        return f'{self.id} of {self.user.username}'


class Action(models.Model):
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )
    date = models.DateTimeField(auto_now=True)
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='actions'
    )

    def __str__(self):
        return f'Account number {self.account.id} was changed on {str(self.amount)}'

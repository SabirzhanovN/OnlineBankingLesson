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

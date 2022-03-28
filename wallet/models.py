from django.db import models
from django.contrib.auth.models import User 

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.IntegerField(default=0, null=False)

    def __str__(self):
        return f"Employee {self.user.first_name} {self.user.last_name} has {self.balance} left"
from django.db import models

# Create your models here.

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=122)
    mob = models.IntegerField()
    password = models.CharField(max_length=122, unique=True)
    email = models.CharField(max_length=122)

class Wallet(models.Model):
    user_id = models.IntegerField()
    amount = models.IntegerField(default=0)

class Transactions(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    amount = models.IntegerField(default=0)
    timestamp = models.DateTimeField()
    payment_id = models.CharField(max_length=122)
    status = models.CharField(max_length=122, default='None')



from django.db import models

class ApiTokens(models.Model):
    username = models.CharField(max_length=20,primary_key=True)
    token = models.CharField(max_length=150)
    expiry = models.CharField(max_length=150)
    active = models.IntegerField()
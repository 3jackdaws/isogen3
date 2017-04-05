from django.db.models import Model
from django.db import models


class Pair(Model):
    key = models.CharField(max_length=64, db_index=True)
    value = models.CharField(max_length=60000)

class APIConsumer(Model):
    token = models.CharField(max_length=32)
    token_date = models.DateTimeField()
    date_joined = models.DateTimeField(auto_created=True)
    identifier = models.CharField(max_length=64)
    email = models.EmailField()

class APIAccessRecord(Model):
    endpoint = models.CharField(max_length=32)
    access_time = models.DateTimeField(auto_created=True)
    consumer = models.ForeignKey(APIConsumer)


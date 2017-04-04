from django.db.models import Model
from django.db import models


class Pair(Model):
    key = models.CharField(max_length=64, db_index=True)
    value = models.CharField(max_length=60000)

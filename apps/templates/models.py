from django.db.models import Model
from django.db import models
import isogen.settings
import re
import random

class EmailReplacement(Model):
    name = models.CharField(max_length=32)
    replacement_string = models.CharField(max_length=32)
    description = models.CharField(max_length=400)
    list_order_priority = models.IntegerField(choices=(1,2,3,4,5,6,7,8,9))

class EmailTemplate(Model):
    title = models.CharField(max_length=64)
    body = models.CharField(max_length=60000)
    replacements = models.ManyToManyField(EmailReplacement)

    def format(self):
        for replacement in self.replacements.all():
            substring = replacement.replacement_string




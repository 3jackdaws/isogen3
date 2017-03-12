from django.db.models import Model
from django.db import models
import isogen.settings


class Stickynote(Model):
    content = models.CharField(max_length=512)
    style = models.CharField(max_length=1024)
    x = models.IntegerField()
    y = models.IntegerField()
    z = models.IntegerField()

class ChatSpam(Model):
    text = models.CharField(max_length=2000)

class DiscussionTopic(Model):
    name = models.CharField(max_length=200)
    url = models.URLField(blank=True)
from django.db.models import Model
from django.db import models

class Procedure(Model):
    script = models.FileField(upload_to="procedures")

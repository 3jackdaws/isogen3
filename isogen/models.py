from django.db.models import Model
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django import forms
from django.utils.html import escape


from isogen.settings import STATIC_URL

# Create your models here.

class Tag(Model):
    class Meta:
        app_label = 'isogen'

    name = models.CharField(max_length=32)
    def __str__(self):
        return self.name

class DirectoryEntry(Model):
    url = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=400)
    icon = models.CharField(max_length=32, default="fa-leaf")
    priority = models.SmallIntegerField()

    def __str__(self):
        return self.title



class ProjectStatus(Model):
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=200)
    def __str__(self):
        return self.name



class Project(Model):
    contributors = models.ManyToManyField(User)
    url = models.URLField(verbose_name="Project URL")
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(default=None, null=True, blank=True)
    status = models.ForeignKey(ProjectStatus)
    technologies = models.ManyToManyField(Tag)

    date_joined = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ProjectUpdates(Model):
    project = models.ForeignKey(Project)
    description = models.CharField(max_length=2000)
    date = models.DateTimeField(default=timezone.now)

class File(Model):
    file = models.FileField()
    members_allowed = models.ManyToManyField(User, default=None, blank=True)
    date_added = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, default=None, blank=True)

    def __str__(self):
        return self.file.name

    def contents(self):

        try:
            content = open(self.file.path).read()
            return escape(content)
        except Exception as e:
            return "This file type cannot be displayed here."



class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"class":"input"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"input"}))
    action = "Login"

class LogoutForm(forms.Form):
    action = "Logout"

from django.db.models import Model
from django.db import models
import isogen.settings
from isogen.models import IsogenMember, Tag
import misaka


class BlogPost(Model):
    author = models.ManyToManyField(IsogenMember)
    datetime_posted = models.DateTimeField()
    datetime_updated = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=140)
    subtitle = models.CharField(max_length=400)
    body = models.TextField()
    header_picture = models.ImageField(blank=True)
    post_tags = models.ManyToManyField(Tag, blank=True)
    featured = models.BooleanField(default=False)
    def __str__(self):
        return self.title

    def get_tags_str(self):
        return " ".join([str(x) for x in self.post_tags.all()])

    def get_body_html(self):
        return misaka.html(self.body)



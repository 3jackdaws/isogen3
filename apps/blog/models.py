from django.db.models import Model
from django.db import models
import isogen.settings
from isogen.models import IsogenMember, Tag
import misaka
from pygments import highlight
from pygments.formatters import ClassNotFound, HtmlFormatter
from pygments.lexers import get_lexer_by_name
import re
import random


class BlogPost(Model):
    header_picture = models.ImageField(blank=True)
    title = models.CharField(max_length=140)
    subtitle = models.CharField(max_length=400)
    author = models.ManyToManyField(IsogenMember)
    datetime_posted = models.DateTimeField()
    datetime_updated = models.DateTimeField(auto_now=True)
    body = models.TextField()
    related_posts = models.ManyToManyField("BlogPost", blank=True)
    post_tags = models.ManyToManyField(Tag, blank=True)
    featured = models.BooleanField(default=False)
    url = models.CharField(editable=False, unique=True, max_length=64, default=None, null=True)

    def __str__(self):
        return self.title

    def get_tags_str(self):
        return " ".join([str(x) for x in self.post_tags.all()])

    def get_body_html(self):
        renderer = HighlighterRenderer()
        md = misaka.Markdown(renderer, extensions=('fenced-code',))
        return md(self.body)

    def get_authors_text(self):
        return ", ".join([x.fullname() for x in self.author.all()])

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.url = re.sub("[^a-zA-Z0-9-]", "", str(self.title).replace(" ", "-"))
        super(BlogPost, self).save()


class HighlighterRenderer(misaka.HtmlRenderer):
    def blockcode(self, text, lang):
        try:
            lexer = get_lexer_by_name(lang, stripall=True)
        except ClassNotFound:
            lexer = None

        if lexer:
            formatter = HtmlFormatter()
            return highlight(text, lexer, formatter)
        # default
        return '\n<pre><code>{}</code></pre>\n'.format(
                            text.strip())

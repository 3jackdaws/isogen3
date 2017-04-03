from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^(find/.+)?$', views.blog),
    url(r'^post/([a-zA-Z0-9-_]+)', views.blog_post)
]
from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^(find/.+)?$', views.blog),
    url(r'^post/([0-9]+)', views.blog_post)
]
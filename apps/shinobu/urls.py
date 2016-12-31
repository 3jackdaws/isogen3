from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'webhook', views.webhook),
    url(r'kv/(.+)/([a-z0-9/-_]+)?', views.kvstore)
]
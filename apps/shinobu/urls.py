from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'webhook', views.webhook),
    url(r'procedure/([a-z0-9A-Z]+)/([a-zA-Z0-9/]+)', views.procedures),
    url(r'kv/(.+)/([a-z0-9/-_]+)?', views.kvstore)
]
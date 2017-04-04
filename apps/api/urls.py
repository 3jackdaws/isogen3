from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.base),
    url(r'^key/add/(.*)?', views.key_append),
    url(r'^key/get/(.*)?', views.key_get),

]
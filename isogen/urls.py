from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'directory/', views.directory, name='directory'),
    url(r'download/', views.downloads, name='downloads'),
    url(r'members/?([a-zA-Z0-9]+)?', views.members, name='downloads'),
    url(r'admin/', admin.site.urls),

    url(r'login/', views.user_login, name='login'),
    url(r'logout/', views.user_logout, name='logout'),
]
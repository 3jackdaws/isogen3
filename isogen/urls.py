from django.conf.urls import url, include
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^$', views.directory),
    url(r'^directory/?(.+)?', views.directory, name='directory'),
    url(r'^download/?', views.downloads, name='downloads'),
    url(r'^get/([a-zA-Z0-9-_]+)', views.get),
    url(r'^members/?([a-zA-Z0-9]+)?', views.members),
    url(r'^me/', views.me),
    url(r'^contact', views.error_ni),
    url(r'^admin/', admin.site.urls),
    url(r'^register/(ajax)?', views.register),
    url(r'^login/?', views.user_login, name='login'),
    url(r'^logout/?', views.user_logout, name='logout'),
    url(r'^error/([0-9]+)', views.error),



    url(r'^meme/', include("apps.memes.urls")),
    url(r'^shinobu/', include("apps.shinobu.urls")),

    url(r'.', views.error_nf, name='error'),
]

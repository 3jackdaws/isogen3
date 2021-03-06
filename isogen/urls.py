from django.conf.urls import url, include
from django.contrib import admin

from isogen import views

urlpatterns = [
    url(r'^(find/.+)?$', views.directory),
    url(r'^api/', include("apps.api.urls")),
    url(r'^directory/(find/.+)?', views.directory, name='directory'),
    url(r'^files/([a-zA-Z0-9._-]+)?', views.files),
    url(r'^get/?([a-zA-Z0-9-_]+)?', views.get),
    url(r'^put/', views.accept_file),
    url(r'^blog/', include("apps.blog.urls")),
    url(r'^status/', views.health_page),
    url(r'^pair/', views.pair),
    url(r'^members/?([a-zA-Z0-9]+)?', views.members),
    url(r'^me/', views.me),
    url(r'^contact', views.error_ni),
    url(r'^admin/', admin.site.urls),
    url(r'^register/(ajax)?', views.register),
    url(r'^login/?', views.user_login, name='login'),
    url(r'^logout/?', views.user_logout, name='logout'),
    url(r'^error/([0-9]+)', views.error),

    url(r'^shinobu/', include("apps.shinobu.urls")),

    url(r'.', views.error_nf, name='error'),
]

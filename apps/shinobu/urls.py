from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'webhook', views.webhook),
    url(r'protocredit', views.protocredit),
    url(r'reichlist', views.reichlist),
    url(r'notes', views.notes),
    url(r'chatspam/new', views.chat_spam_add),
    url(r'chatspam', views.chat_spam),
    url(r'discussion/([a-z0-9A-Z]+)?', views.discussion),
    url(r'trash/([a-zA-Z0-9]+)', views.trash_duty),

    url(r'kv/(.+)/([a-z0-9/-_]+)?', views.kvstore)
]
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from isogen.views import get_nav_form, get_user
from apps.blog.models import BlogPost

def index(request, search=None):
    user = get_user(request)
    if search:
        pass
    else:
        pass
    context = {
        "title": "Email Templates",
        "login_form": get_nav_form(request),
        "user": user,
        "posts": posts,
        "most_recent": most_recent,
        "search": search
    }
    return render(request, 'blog/homepage.html', context)

def template_view(request, template):
    pass
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from isogen.views import get_nav_form, get_user
from apps.blog.models import BlogPost
import pymysql
from isogen.settings import DATABASES, BASE_DIR

def blog(request):
    user = get_user(request)
    posts = BlogPost.objects.order_by("datetime_posted")
    context = {
        "title": "Recent Posts - ISOGEN Blog",
        "login_form": get_nav_form(request),
        "user": user,
        "posts":posts
    }
    return render(request, 'blog/homepage.html', context)

def blog_post(request, id):
    user = get_user(request)
    post = BlogPost.objects.get(id=id)
    footer_posts = BlogPost.objects.order_by("datetime_posted")[:3]
    context = {
        "title": "{} - ISOGEN Blog".format(post.title),
        "login_form": get_nav_form(request),
        "user": user,
        "post":post,
        "footer_posts":footer_posts
    }
    return render(request, 'blog/post.html', context)
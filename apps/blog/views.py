from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from isogen.views import get_nav_form, get_user
from apps.blog.models import BlogPost
import pymysql
from isogen.settings import DATABASES, BASE_DIR

def blog(request, search=None):
    user = get_user(request)
    posts = []
    most_recent = None
    featured = None
    if search:
        search = search.rsplit("/")[1].lower()
        for post in BlogPost.objects.order_by("-datetime_posted"):
            if search in post.title.lower() \
                    or search in post.subtitle.lower() \
                    or search in post.get_tags_str().lower()\
                    or search in post.get_authors_text().lower():
                posts.append(post)
    else:
        posts = BlogPost.objects.order_by("-datetime_posted")
        try:
            featured = posts.filter(featured=True)[0]
        except:
            pass
        posts = posts.exclude(id=featured.id)
        most_recent = posts[0:3]
        posts = posts[3:12]

    context = {
        "title": "Recent Posts - ISOGEN Blog",
        "login_form": get_nav_form(request),
        "user": user,
        "posts":posts,
        "featured":featured,
        "most_recent":most_recent,
        "search": "" if search is None else search
    }
    return render(request, 'blog/homepage.html', context)

def blog_post(request, name):
    user = get_user(request)
    post = BlogPost.objects.get(url=name)
    footer_posts = list(post.related_posts.all()[:3])
    num_req = 3 - len(footer_posts)
    if num_req > 0:
        footer_posts.extend(list(BlogPost.objects.order_by("-datetime_posted")[:num_req]))
    context = {
        "title": "{} - ISOGEN Blog".format(post.title),
        "login_form": get_nav_form(request),
        "user": user,
        "post":post,
        "footer_posts":footer_posts
    }
    return render(request, 'blog/post.html', context)
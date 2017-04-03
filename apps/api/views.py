from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from isogen.views import get_nav_form, get_user
from apps.blog.models import BlogPost
import pymysql
from isogen.settings import DATABASES, BASE_DIR

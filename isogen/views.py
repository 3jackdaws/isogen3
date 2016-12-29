from django.shortcuts import render, HttpResponse
import os, tempfile, zipfile
from django.template import loader
from wsgiref.util import FileWrapper
from isogen.models import DirectoryEntry, Project, ProjectUpdates, File, LoginForm, LogoutForm
from isogen.settings import MEDIA_ROOT
from django.contrib.auth import logout, login, authenticate
import json



# Create your views here.
def index(request):
    # try:
    #     featured = Project.objects.get(featured=1)
    # except:
    #     pass
    projects = Project.objects.order_by("name")
    user = None
    if request.user.is_authenticated():
        user = request.user
    context = {'projects': projects, "title": "Home - ISOGEN", "login_form":get_nav_form(request), "user":user}
    return render(request, 'projects.html', context)

def directory(request):
    user = None
    if request.user.is_authenticated():
        user = request.user
    sites = DirectoryEntry.objects.order_by('priority')[:5]
    context = {'sites': sites, "title":"Directory - ISOGEN", "login_form":get_nav_form(request), "user":user}
    return render(request, 'directory.html', context)

def get_nav_form(request):
    if request.user.is_authenticated():
        login_logout_form = LogoutForm
    else:
        login_logout_form = LoginForm
    return login_logout_form

def downloads(request):
    user = None
    if request.user.is_authenticated():
        user = request.user
    # files = File.objects.all()
    files = [x for x in File.objects.all() if user in x.members_allowed.all() or len(x.members_allowed.all()) == 0]

    context = {'files': files, "title": "Downloads - ISOGEN", "login_form":get_nav_form(request), "user":user}
    return render(request, 'downloads.html', context)


def send_file(request, filename):
    """
    Send a file through Django without loading the whole file into
    memory at once. The FileWrapper will turn the file object into an
    iterator for chunks of 8KB.
    """
    filename = MEDIA_ROOT + filename
    wrapper = FileWrapper(open(filename))
    response = HttpResponse(wrapper, content_type='text/plain')
    response['Content-Length'] = os.path.getsize(filename)
    return response

def user_login(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = LoginForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponse(json.dumps({"success":True}))
    return HttpResponse(json.dumps({"success":False}))

def user_logout(request):
    if request.user.is_authenticated():
        logout(request)
        return HttpResponse(json.dumps({"success": True}))


def members(request, member):
    return HttpResponse(member)

def error(request, number):
    error_msg = ""
    msgs = {404:"It looks like you're lost.", 403:"That's not allowed :^)", 501:"This page doesn't exist yet."}
    if number in msgs:
        error_msg = msgs[number]
    context = {"title": "Error - ISOGEN", "error_code":number, "error_msg":error_msg}
    return render(request, 'error.html', context)

def error_nf(request):
    return error(request, 404)

def error_ni(request, *args):
    return error(request, 501)

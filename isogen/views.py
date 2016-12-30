from django.shortcuts import render, HttpResponse, HttpResponseRedirect
import os, tempfile, zipfile
from django.template import loader
from wsgiref.util import FileWrapper
from isogen.models import DirectoryEntry, Project, ProjectUpdates, File, LoginForm, LogoutForm, MemberRegisterForm, IsogenMember
from isogen.settings import MEDIA_ROOT
from django.contrib.auth import logout, login, authenticate
import json
from django.contrib.auth.models import User, Group



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

def directory(request, search=None):
    user = None
    if request.user.is_authenticated():
        user = request.user
    if search is not None:
        sites = []
        for site in DirectoryEntry.objects.order_by("priority"):
            if search.lower() in site.title.lower() or search.lower() in site.description.lower():
                sites.append(site)
    else:
        sites = DirectoryEntry.objects.order_by("priority")

    context = {'sites': sites, "title":"Directory - ISOGEN", "login_form":get_nav_form(request), "user":user, "search":search}
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


def members(request, member=None):
    if member is None:
        member_list = IsogenMember.objects.all()
    else:
        member_list = [User.objects.get(username=member)]
    context = {"title": "Members - ISOGEN", "member_list":member_list}
    return render(request, 'members.html', context)

def register(request, ajax = False):
    def did_reg(form):
        if form.is_valid():
            username = request.POST['username']
            email = request.POST['email']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            password = request.POST['password']
            user = User.objects.create_user(username, email, password, first_name=first_name, last_name=last_name)
            member = IsogenMember(user=user)
            login(request, user)
            return True
        else:
            return False

    if request.method == 'POST':
        form = MemberRegisterForm(request.POST)
        if did_reg(form):
            if ajax:
                return HttpResponse(json.dumps({
                    "action":"register",
                    "success":True
                }))
            else:
                return HttpResponse(json.dumps({
                    "action": "register",
                    "success": True,
                    "redirect":"/me/"
                }))
        else:
            if ajax:
                return HttpResponse(json.dumps({
                    "action": "register",
                    "success": False,
                    "errors":str(form.errors)
                }))
            else:
                return HttpResponse("That didn't work :(")
    else:
        context = {"title": "Register - ISOGEN", "register_form":MemberRegisterForm}
        return render(request, 'register.html', context)



def me(request):
    user = None
    if request.user.is_authenticated():
        user = request.user
        member = IsogenMember.objects.get(user=user)
        context = {"title": "Your Account - ISOGEN", "user": user, "member":member, "login_form":get_nav_form(request)}
        return render(request, 'me.html', context)
    else:
        return HttpResponse("You must login to view this page.")

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

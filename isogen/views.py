from django.shortcuts import render, HttpResponse, HttpResponseRedirect
import os, tempfile, zipfile
from django.template import loader
from wsgiref.util import FileWrapper
from isogen.models import DirectoryEntry, Project, ProjectUpdates, File, LoginForm, LogoutForm, MemberRegisterForm, IsogenMember
from isogen.settings import MEDIA_ROOT
from django.contrib.auth import logout, login, authenticate
import json
from django.contrib.auth.models import User, Group
from django.http.request import HttpRequest
from django.core.files.uploadhandler import InMemoryUploadedFile
from django.core.files import File as DjangoFile


# Create your views here.
# no u
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

def get_user(request):
    return request.user if request.user.is_authenticated() else None

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
    context = {"title": "Downloads - ISOGEN", "login_form":get_nav_form(request), "user":user}
    return render(request, 'downloads.html', context)


def files_available(request):
    user = None
    if request.user.is_authenticated():
        user = request.user
    # files = File.objects.all()
    visible_files = []
    for file in File.objects.all():
        if user in file.members_allowed.all() or len(file.members_allowed.all()) == 0:
            try:
                file.file.size

                visible_files.append(file)
            except Exception as e:
                print(e)
                pass

    context = {'files': visible_files}
    return render(request, 'components/available_files.html', context)


def send_file(request, filename):
    """
    Send a file through Django without loading the whole file into
    memory at once. The FileWrapper will turn the file object into an
    iterator for chunks of 8KB.
    """
    wrapper = FileWrapper(open(filename, "rb"))
    response = HttpResponse(wrapper, content_type='download')
    response['Content-Length'] = os.path.getsize(filename)
    response['Content-Disposition'] = 'attachment; filename=%s' % os.path.basename(filename)
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
    number = int(number)
    msgs = {
        404: "It looks like you're lost.",
        401: "You're not allowed here :^)",
        403: "I'm afraid I can't do that, Dave.",
        501: "This page doesn't exist yet."}
    if number in msgs:
        error_msg = msgs[number]
    context = {"title": "Error - ISOGEN", "error_code":number, "error_msg":error_msg}
    return render(request, 'error.html', context, status=number)

def error_nf(request):
    return error(request, 404)

def error_ni(request, *args):
    return error(request, 501)

def error_403(request):
    return error(request, 403)

def user_can_access_file(user, file):
    if user in file.members_allowed.all() or len(file.members_allowed.all()) == 0:
        return True
    return False

def json_response(request, obj):
    return HttpResponse(json.dumps(
            obj,
            indent=2
        ), content_type='application/json')

def get(request, fileid=None):
    authenticated_user = None
    if request.user.is_authenticated():
        authenticated_user = request.user
    if fileid:
        try:
            requested_file = File.objects.get(id=fileid)
        except:
            return error_403(request)

        if user_can_access_file(authenticated_user, requested_file):

            file_path = requested_file.file.path

            return send_file(request, file_path)

        else:
            return error_403(request)

    else:
        visible_files = []
        all_files = File.objects.all()
        for file in all_files:
            if user_can_access_file(authenticated_user, file):
                visible_files.append(file)
        file_json_response = []

        for file in visible_files:
            file_json_response.append({
                "name":file.file.name,
                "url":"https://isogen.net/get/"+str(file.id),
                "description":file.description,
                "restricted_to":[str(x) for x in file.members_allowed.all()]
            })


        return json_response(request, file_json_response)


    # files = File.objects.all()


def accept_file(request):
    authenticated_user = None
    if request.user.is_authenticated() and "uploadedFile" in request.FILES:
        authenticated_user = request.user

        file = request.FILES["uploadedFile"] #type: InMemoryUploadedFile

        db_file = File()

        db_file.file.save(
            file.name,
            DjangoFile(file)
        )

        response = {
            "action": "file-upload",
            "result": "success",
            "name": file.name
        }
    else:
        response = {
            "action": "file-upload",
            "result": "failure"
        }

    return json_response(request, response)





from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.http import HttpRequest
from isogen.views import get_nav_form, json_response
from apps.shinobu.models import Stickynote, ChatSpam
import pymysql
from isogen.settings import DATABASES, BASE_DIR
import sys

def index(request):
    return HttpResponse("heelo")

def webhook(request):
    user = None
    if request.user.is_authenticated():
        user = request.user
    context = {"title": "Discord Webhook Executor", "login_form": get_nav_form(request), "user": user}
    return render(request, 'shinobu/webhook.html', context)

def kvstore(request, token, key=None):
    connection = pymysql.Connect(host=DATABASES['kv']['HOST'],
                                 db=DATABASES['kv']['NAME'],
                                 user=DATABASES['kv']['USER'],
                                 password=DATABASES['kv']['PASSWORD'],
                                 cursorclass=pymysql.cursors.DictCursor)
    if request.method == 'POST':
        pass
    else:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM kv a "
                       "LEFT JOIN kv b "
                       "ON a.v = b.k "
                       "WHERE a.user_id = %s ", (token))

        results= cursor.fetchall()
        return HttpResponse(str(results))

def procedures(request, procedure, args):
    sys.path.append(BASE_DIR + "/static/media/procedures/")
    try:
        module = __import__(procedure)
        parameters = args.rsplit("/")
        output = module.function(*parameters)
    except Exception as e:
        output = str(e)
    return HttpResponse(output)

def get_shinobu_db_cursor():
    db = DATABASES['default']
    connection = pymysql.Connect(host=db['HOST'],
                                 user=db['USER'],
                                 password=db['PASSWORD'],
                                 database='shinobu',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection.cursor()

def reichlist(request):
    user = None
    if request.user.is_authenticated():
        user = request.user
    cursor = get_shinobu_db_cursor()
    results = cursor.execute("SELECT * FROM Reichlist JOIN Accounts ON Accounts.UserID = Reichlist.ItemContributor")
    entries = cursor.fetchall()
    context = {"title": "Shinobu Reichlist Entries", "login_form": get_nav_form(request), "user": user, "entries":entries}
    return render(request, 'shinobu/reichlist.html', context)

def notes(request):
    user = None
    if request.user.is_authenticated():
        user = request.user
    stickynotes = Stickynote.objects.all()
    context = {"title": "Sticky Notes", "login_form": get_nav_form(request), "user": user, "notes":stickynotes}
    return render(request, 'shinobu/stickynotes.html', context)


def protocredit(request):
    user = None
    if request.user.is_authenticated():
        user = request.user
    stickynotes = Stickynote.objects.all()
    context = {"title": "Protocredits", "login_form": get_nav_form(request), "user": user}
    return render(request, 'shinobu/protocredits.html', context)

def chat_spam(request:HttpRequest, category=None):
    favorites = request.COOKIES.get("favorites")
    print(favorites)
    cards = None
    if favorites is not None:
        pass
    cards = ChatSpam.objects.all()
    context = {
        "title": "Chat spam",
        "login_form": get_nav_form(request),
        "user": request.user if request.user.is_authenticated() else None,
        "chat_cards":cards
    }
    return render(request, 'shinobu/chat_spam.html', context)

def chat_spam_add(request:HttpRequest):
    text = request.POST.get("text")
    if text:
        ChatSpam.objects.create(text=text)
        response_text = "success"
    else:
        response_text = "failure"
    return json_response(request, {
        "result":response_text
    })


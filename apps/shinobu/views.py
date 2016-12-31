from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from isogen.views import get_nav_form
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
        output += "<br>" + str(sys.path)
    return HttpResponse(output)
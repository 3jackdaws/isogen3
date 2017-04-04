from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from isogen.views import get_nav_form, get_user, json_response
from .models import *
from isogen.settings import DATABASES, BASE_DIR

def base(request):
    obj = {
        "Version":"1.0.0",
        "resource":"Isogen API"
    }
    return json_response(request, obj)

@csrf_exempt
def pair(request, key=None):
    obj = {}
    if request.POST:
        for key in request.POST:
            print(key)
            if key not in obj:
                obj[key] = []
            obj[key].append(Pair.objects.create(key=key, value=request.POST[key]).value)
    else:
        pairs = Pair.objects.all().filter(key=key)
        obj[key] = [x.value for x in list(pairs)]

    return json_response(request, obj)
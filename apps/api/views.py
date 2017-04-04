from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from isogen.views import get_nav_form, get_user, json_response
from .models import *
from isogen.settings import DATABASES, BASE_DIR
from isogen.utils import background





def base(request):
    obj = {
        "Version":"1.0.0",
        "resource":"Isogen API"
    }
    return json_response(request, obj)

KV_CACHE = {}

@csrf_exempt
def pair(request, key=None):
    obj = {}
    if request.POST:
        for key in request.POST:
            # print(key)
            if key not in KV_CACHE:
                pairs = Pair.objects.all().filter(key=key)
                KV_CACHE[key] = [x.value for x in list(pairs)]
                new = Pair(key=key, value=request.POST[key])
                KV_CACHE[key].append(new.value)
                background(new.save)
            obj[key] = KV_CACHE[key]
    else:
        if key not in KV_CACHE:
            pairs = Pair.objects.all().filter(key=key)
            KV_CACHE[key] = [x.value for x in list(pairs)]
        obj[key] = KV_CACHE[key]

    return json_response(request, obj)
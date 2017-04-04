from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from isogen.views import get_nav_form, get_user, json_response
from .models import *
from isogen.settings import DATABASES, BASE_DIR
from isogen.utils import queue_task, test_print





def base(request):
    obj = {
        "Version":"1.0.0",
        "resource":"Isogen API"
    }
    return json_response(request, obj)

KV_CACHE = {}

def get(key):
    pass


@csrf_exempt
def pair(request, key=None):
    obj = {}
    if request.POST:
        for key in request.POST:
            # print(key)
            if key not in KV_CACHE:
                pairs = Pair.objects.all().filter(key=key)
                print("Cache miss")
                KV_CACHE[key] = [{"text":x.value, "id":x.id} for x in list(pairs)]

            else:
                print("Cache hit")
            new = Pair(key=key, value=request.POST[key])
            KV_CACHE[key].append({"text":new.value, "id":new.id})
            queue_task(test_print, new.save, "saving")
            obj[key] = KV_CACHE[key]
    else:
        if key not in KV_CACHE:
            pairs = Pair.objects.all().filter(key=key)
            KV_CACHE[key] = [{"text":x.value, "id":x.id} for x in list(pairs)]
        obj[key] = KV_CACHE[key]

    return json_response(request, obj)



@csrf_exempt
def key_append(request, key):
    # print(key)
    if "text" in request.POST:

        new = Pair(key=key, value=request.POST["text"])
        queue_task(save_then_load, new, key)
        return json_response(request, {
            key: request.POST["text"]
        })
    else:
        return JsonResponse({
            "error":"Bad request",
            "reason":"'text' not found in POST data"
        }, json_dumps_params={"indent":2}, status=400)

def key_get(request, key):
    if key not in KV_CACHE:
        pairs = Pair.objects.all().filter(key=key)
        KV_CACHE[key] = [{"text": x.value, "id": x.id} for x in list(pairs)]
    return JsonResponse({key:KV_CACHE[key]}, json_dumps_params={"indent":2})

def save_then_load(model_object, key):
    global KV_CACHE
    if key not in KV_CACHE:
        pairs = Pair.objects.all().filter(key=key)
        KV_CACHE[key] = [{"text":x.value, "id":x.id} for x in list(pairs)]
    else:
        model_object.save()
        KV_CACHE[key].append({"text":model_object.value, "id":model_object.id})

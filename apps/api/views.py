from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from isogen.views import get_nav_form, get_user, json_response
from .models import *
from isogen.settings import DATABASES, BASE_DIR
from isogen.utils import async_run, async_defer, test_print, cache
import time
import datetime




cache.kv = {}
cache.consumer = {}
KV_CACHE = {}
STATS = {
    "/api/"         :{ "requests":0, "total-time":0 },
    "/api/key/get/" :{ "requests":0, "total-time":0 },
    "/api/key/add/" :{ "requests":0, "total-time":0 },
}


def base(request):
    obj = {
        "Version":"1.0.0",
        "resource":"Isogen API"
    }
    return JsonResponse(obj, json_dumps_params={"indent":2})


def get(key):
    pass

def get_consumer(token):
    consumer = None
    if token not in cache.consumer:
        consumer = APIConsumer.objects.get(token=token)
        cache.consumer[token] = consumer
        return consumer
    else:
        return cache.consumer[token]


# @csrf_exempt
# def pair(request, key=None):
#     obj = {}
#     if request.POST:
#         for key in request.POST:
#             # print(key)
#             if key not in KV_CACHE:
#                 pairs = Pair.objects.all().filter(key=key)
#                 print("Cache miss")
#                 KV_CACHE[key] = [{"text":x.value, "id":x.id} for x in list(pairs)]
#
#             else:
#                 print("Cache hit")
#             new = Pair(key=key, value=request.POST[key])
#             KV_CACHE[key].append({"text":new.value, "id":new.id})
#             async_run(test_print, new.save, "saving")
#             obj[key] = KV_CACHE[key]
#     else:
#         if key not in KV_CACHE:
#             pairs = Pair.objects.all().filter(key=key)
#             KV_CACHE[key] = [{"text":x.value, "id":x.id} for x in list(pairs)]
#         obj[key] = KV_CACHE[key]
#
#     return json_response(request, obj)


@csrf_exempt
def key_append(request, key):
    consumer = get_consumer(request.COOKIES['token'])
    response = {}
    status = 200
    if not consumer:
        response['error'] = "Not authorized"
        status = 403
    if "text" in request.POST:
        new = Pair(key=key, value=request.POST["text"])
        async_run(save_then_load, new, key)
        response = {
            key: request.POST["text"]
        }
    else:
        response['error'] = "'text' not in POST body"
        response['status'] = 'bad request'
        status = 400
    return JsonResponse(response, json_dumps_params={"indent":2}, status=status)

def key_get(request, key):
    if key not in cache.kv:
        pairs = Pair.objects.all().filter(key=key)
        cache.kv[key] = [{"text": x.value, "id": x.id} for x in list(pairs)]
    return JsonResponse({key:cache.kv[key]}, json_dumps_params={"indent":2})

def save_then_load(model_object, key):
    if key not in cache.kv:
        pairs = Pair.objects.all().filter(key=key)
        cache.kv[key] = [{"text":x.value, "id":x.id} for x in list(pairs)]
    else:
        model_object.save()
        cache.kv[key].append({"text":model_object.value, "id":model_object.id})

from django.shortcuts import render
from django.http import JsonResponse
from hour_app.models import Topic
# Create your views here.

def test(request):
    routes = [
        'Get /api/rooms'
        'Get /api/rooms/:id'
    ]
    return JsonResponse(routes, safe=False)
def topics(reqeust):
    return JsonResponse(str(Topic.objects.all()), safe=False)
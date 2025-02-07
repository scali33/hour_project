from django.shortcuts import render
from django.http import JsonResponse
from hour_app.models import Topic
from rest_framework.decorators import api_view
from rest_framework.response import Response
from hour_app.models import Room
from .serializers import RoomSerializer
# Create your views here.
@api_view(['GET'])
def test(request):
    routes = [
        'Get /api/rooms'
        'Get /api/rooms/:id',
        'GEt /api'
    ]
    return Response(routes)
@api_view(['GET'])
def rooms(reqeust):
    rooms_var = Room.objects.all()
    serialized = RoomSerializer(rooms_var, many=True)
    return Response(serialized.data)

@api_view(['GET'])
def one_room(reqeust,pk):
    room = Room.objects.get(id=pk)
    serialized = RoomSerializer(room, many=False)
    return Response(serialized.data)
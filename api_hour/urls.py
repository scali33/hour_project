from django.urls import path
from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import views

urlpatterns = [
    path('',views.test, name='Default'),
    path('rooms/', views.rooms, name='rooms'),
     path('room/<str:pk>/', views.one_room, name='one_room')
]
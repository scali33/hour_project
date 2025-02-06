from django.urls import path
from . import views

urlpatterns = [
    path('',views.test, name='Default'),
    path('topics', views.topics, name='topics')
]
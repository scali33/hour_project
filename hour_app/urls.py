from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage,name='login_page'),
    path('logout/', views.logoutUser, name='logout_fun'),
    path('register/', views.registerUser,name='register'),
    path('',views.home, name='home'),
    path('room/<str:sala_id>/', views.room,  name='backroom'),
    path('create-room',views.create_room, name='make_room'),
    path('update-room/<str:pk>',views.updateRoom, name='update_room'),
    path('delete-room/<str:pk>', views.delete_room, name='delete-room'),
    path('delete-message/<str:pk>', views.delete_message, name='delete-message'),
    path('profile/<str:pk>', views.userProfile, name='user_profile'),
    path('update-user/<str:pk>', views.update_profile, name='update_user'),
    path('topics/',views.topics_view,name='topics_page'),
    path('activiy/', views.activity_feed_view, name='activiy_page')

    
]
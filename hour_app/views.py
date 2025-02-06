from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import Room,Topic,Message
from django.db.models import Q
from .froms import RoomForm, Userform
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
#rooms = [
#    {'id':1, 'name':'lets learn python' },
#    {'id':2 ,'name':'js is life'},
#    {'id':3,'name':'yo cobol is awsson'}
#]

# Create your views here.
def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        user_name = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username = user_name)
        except:
            messages.error(request, 'User not found')
        user = authenticate(request, username= user_name, password = password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username Or password are not valid ')
    return render(request, 'hour_app/login_register.html', {'page':page})

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerUser(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')
    return render(request, 'hour_app/login_register.html',{'form':form})

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(Q(topic__name__icontains = q) | Q(name__icontains = q) | Q(description__icontains = q) )

    topics = Topic.objects.all()[0:5]
    room_counts = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    return render(request, 'hour_app/home.html', {'rooms': rooms,'topics':topics, 'room_count':room_counts, 'room_massages':room_messages})

def room(request,sala_id):
    room = Room.objects.get(id = sala_id )
    roomMessages = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    if request.method == "POST":
        message = Message.objects.create(
            user = request.user,
            room= room,
            body= request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('backroom', sala_id=room.id)
    return render(request, 'hour_app/room.html', {'room':room,'roomMessages':roomMessages,'participants':participants})

@login_required(login_url='/login')
def create_room(request):
    form = RoomForm()
    topics = Topic.objects.all()

    if request.method == 'POST': 
       topic_name = request.POST.get('topic')
       topic, created = Topic.objects.get_or_create(name=topic_name)
       Room.objects.create(
           host=request.user,
           topic = topic,
           name=request.POST.get('name'),
           description=request.POST.get('description'))
       return redirect('home')
    return render(request, 'hour_app/room_form.html', {'form':form,'topics':topics,'UorC':'Create'})

@login_required(login_url='/login')
def updateRoom(request, pk):
    topics = Topic.objects.all()
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    
    if request.user != room.host :
        return HttpResponse('Youre not the room creator! ')

    if request.method == "POST":
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
    return render(request, 'hour_app/room_form.html', {'form':form, 'topics': topics, 'room':room,'UorC':'update'})

@login_required(login_url='/login')
def delete_room(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host :
        return HttpResponse('You are forbidden ')
    
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'hour_app/delete.html',{'obj':room})

@login_required(login_url='/login')
def delete_message(request, pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user :
        return HttpResponse('Youre forbidden')
    
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'hour_app/delete.html',{'obj':message})
def userProfile(request,pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    return render(request, 'hour_app/profile.html', {'user':user,'rooms':rooms,'room_massages':room_messages,'topics':topics})

@login_required(login_url='/login')
def update_profile(request,pk):
    user = request.user
    form = Userform(instance=user)
    if request.method == "POST":
        form = Userform(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_profile',pk = user.id)
    return render(request,'hour_app/update-user.html', {'form':form})

def topics_view(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request,'hour_app/topics.html',{'topics':topics})

def activity_feed_view(request):
    room_messages = Message.objects.all()[0:5]
    return render(request,'hour_app/activity.html',{'room_messages': room_messages})
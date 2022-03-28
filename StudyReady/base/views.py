from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .models import Room, Topic, Message, User
from .forms import RoomForm, UserForm, NewUserCreationForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# Create your views here

def home(request):
    page = 'home'

    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.order_by('-updated','-created').filter(
        Q(topic__name__icontains = q) |
        Q(name__icontains = q) |
        Q(description__icontains = q)
    )
    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    recent_messages = Message.objects.order_by('-created','-updated').filter(Q(room__name__icontains=q))

    context = {'rooms': rooms, 'topics':topics,'room_count':room_count,'recent_messages':recent_messages}
    return render(request, 'base/home.html', context)

def room(request, pk):
    page = 'room'
    room = Room.objects.get(id = pk)
    recent_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk = room.id)

    context = {'room': room, 'recent_messages':recent_messages,'participants':participants}
    return render(request,'base/room.html',context)

@login_required(login_url = 'login')
def createRoom(request):
    page = 'create'

    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        # form = RoomForm(request.POST)
        topic_name = request.POST.get('topic')
        topic, create = Topic.objects.get_or_create(name = topic_name)

        Room.objects.create(
            host = request.user,
            topic=topic,
            name=request.POST.get('name'),
            description= request.POST.get('description'),
        )
        return redirect('home')
        
    context = {'form':form ,'topics':topics,'page':page}
    return render(request, 'base/room_form.html',context)

@login_required(login_url = 'login')
def updateRoom(request, pk):
    page = 'update'

    room = Room.objects.get(id = pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, create = Topic.objects.get_or_create(name = topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')

    context = {'form': form, 'topics':topics,'room':room,'page':page}
    return render(request, 'base/room_form.html', context)

def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    context ={'delete_obj': room}
    return render(request, 'base/delete.html',context)

def loginPage(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'A aparut o eroare in crearea contului!')
        user = authenticate(request, email=email,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
    context={'page':page}
    return render(request, 'base/login_register.html',context)

def logoutPage(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    page = 'register'
    form = NewUserCreationForm()

    if request.method == 'POST':
        form = NewUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, 'A aparut o eroare in crearea contului!')

    context = {'page':page, 'form':form}
    return render(request, 'base/login_register.html', context)

def deleteMsg(request, pk):
    message = Message.objects.get(id=pk)

    if request.method == 'POST':
        message.delete()
        return redirect('home')

    context ={'delete_obj': message}
    return render(request, 'base/delete.html',context)

def userProfile(request,pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all().order_by('-created','-updated')
    recent_messages = user.message_set.all()
    topics = Topic.objects.all()[0:5]

    context = {'user':user, 'rooms':rooms,'recent_messages':recent_messages,'topics':topics}
    return render(request, 'base/profile.html', context)

@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance = user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES , instance = user)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form':form}
    return render(request, 'base/update_user.html',context)


def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics =Topic.objects.all().filter(Q(room__name__icontains=q))
    context = {'topics': topics}
    return render(request, 'base/topics.html',context)

def activityPage(request):
    recent_messages = Message.objects.all()
    context = {'recent_messages': recent_messages}
    return render(request, 'base/activity.html',context)









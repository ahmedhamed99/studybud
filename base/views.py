import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt


from .models import  Message, Room, Topic
from .forms import RoomForm, UserForm, User,MyUserCreationForm

# Create your views here.

def loginPage(request):
    if request.method == 'POST':
        email = request.POST["email"].lower()
        password = request.POST["password"]
        
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request,"User does not exist")

        user = authenticate(email=email,password=password)
        if not user:
            messages.error(request,"Email or Password is incorrect")
        else:
            login(request,user)
            return redirect("home")
        
    if request.user.is_authenticated:
        return redirect('home')
    page = 'login'
    return render(request,'base/login_register.html', {'page': page})

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerUser(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.add_message(request,messages.ERROR,"An error occurred during registration.")

    return render(request,'base/login_register.html',{'form': form})

def home(request):
    q = request.GET.get("q") if request.GET.get("q") else ""
    page = request.GET.get('page') if request.GET.get('page') else ""
    rooms = Room.objects.filter(
        Q(topic__name__icontains = q) |
        Q(name__icontains = q) |
        Q(description__icontains = q)
    )
    paginator = Paginator(rooms, 10)
    roomsobj = paginator.get_page(page)

    topics = Topic.objects.all()[0:5]
    roomcount = rooms.count()
    page_range = int((roomcount-1)/10) 
    if page != "":
        range_start = 1 if int(page) <= 5 else int(page)
    else:
        range_start = 1
        
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    
    context = {'rooms': roomsobj,'topics':topics,'roomcount': roomcount,'room_messages': room_messages,'range': range(range_start,page_range+2)}
    return render(request,'base/home.html', context)

def room(request,pk):
    room = Room.objects.get(id=pk)
    room_messages = room.messages.all()[0:25]
    participants = room.participants.all()
    
    if request.method == 'POST':
        if request.POST.get('body'):
            message = Message.objects.create(
                user = request.user,
                room = room,
                body = request.POST['body']
            )
            message.save()
            room.participants.add(request.user)
            return redirect('room', pk=room.id)

        elif request.POST.get('edit'):
            message_id = int(request.POST['edit'])
            context = {'room': room,'room_messages': room_messages,'participants': participants,'editmessage': message_id}
            return render(request,'base/room.html',context)
        
        elif request.POST.get('newmessage'):
            message_id = request.POST['message_id']
            newmessage = request.POST['newmessage']
            message = Message.objects.get(pk=message_id)
            message.body = newmessage
            message.save()
            return redirect('room', pk=room.id)
    

    context = {'room': room,'room_messages': room_messages,'participants': participants}
    return render(request,'base/room.html', context)

def userProfile(request,pk):
    page = request.GET.get('page') if request.GET.get('page') else 1

    user = User.objects.get(pk=pk)
    rooms = user.hostedrooms.all()
    room_messages = user.usermessages.all()

    paginator = Paginator(rooms, 10)
    roomsobj = paginator.get_page(page)

    topics = Topic.objects.all()[0:5]
    roomcount = rooms.count()
    page_range = int((roomcount-1)/10) 
    if page != "":
        range_start = 1 if int(page) <= 5 else int(page)
    else:
        range_start = 1

    context = {'user': user,'rooms': roomsobj,'room_messages': room_messages,'topics': topics,'range': range(range_start,page_range+2),'roomcount': roomcount}
    return render(request,'base/profile.html', context)

@login_required(login_url='/login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()

    if request.method == 'POST':
        topic_name = request.POST['topic']
        topic, created = Topic.objects.get_or_create(
            name=topic_name
        )
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST['name'],
            description = request.POST['description']
        )
        return redirect('home')

    context = {'form': form,'topics':topics}
    return render(request,'base/room_form.html', context)

@login_required(login_url='/login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    if request.user != room.host:
        return HttpResponse('You are not allowed here!')

    if request.method == "POST":
        print('updating')
        topic_name = request.POST['topic']
        topic, created = Topic.objects.get_or_create(
            name=topic_name
        )
        room.name = request.POST['name']
        room.topic = topic
        if request.POST['description'] != '':
            room.description = request.POST['description']
        room.save()
        return redirect('home')
        
    context = {'form': form,'topics': topics,'room':room}
    return render(request,'base/room_form.html',context)

@login_required(login_url='/login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('You are not allowed here!')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    
    return render(request,'base/delete.html',{'obj': room})
    
@login_required(login_url='/login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You are not allowed here!')

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    
    return render(request,'base/delete.html',{'obj': message})

@login_required(login_url=('/login'))
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    
    if request.method == 'POST':
        print('updating')
        try:
            form = UserForm(request.POST, request.FILES ,instance=user)
        except:
            return render(request,'base/update-user.html',{'form': form})
        if form.is_valid():
            print('valid')
            form.save()
            return redirect('user-profile',pk=user.id)
    
    return render(request,'base/update-user.html',{'form': form})

def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') else ''
    topics = Topic.objects.filter(name__icontains = q)
    
    return render(request,'base/topics.html',{'topics': topics})

def activityPage(request):
    room_messages = Message.objects.all()

    return render(request,'base/activity.html',{'room_messages': room_messages})


def followTopic(request,topic_id):
    if request.method == 'PUT':
        data = json.loads(request.body)

        if not request.user.is_authenticated:
            return JsonResponse({"error":f"you must be logged in to {data['method']} topic"})

        topic = Topic.objects.get(id=topic_id)

        if data['method'] == "follow":
            topic.followers.add(request.user)
            topic.save()
        elif data['method'] == "unfollow":
            topic.followers.remove(request.user)
            topic.save()

        return JsonResponse({"message": f"topic {topic.name} {data['method']}ed successfully"})

def followUser(request,user_id):
    if request.method == 'PUT':
        data = json.loads(request.body)
        if not request.user.is_authenticated:
            return JsonResponse({"error":f"you must be logged in to {data['method']} users"})

        followeduser = User.objects.get(id=user_id)
        followinguser = User.objects.get(id=request.user.id)

        if data['method'] == "follow":
            followeduser.followers.add(request.user)
            followinguser.followings.add(followeduser)
            followeduser.save()
            followinguser.save()
        elif data['method'] == "unfollow":
            followeduser.followers.remove(request.user)
            followinguser.followings.remove(followeduser)
            followeduser.save()
            followinguser.save()

        return JsonResponse({"message": f"user {followinguser.username} {data['method']}ed user {followeduser.username} successfulyy"})

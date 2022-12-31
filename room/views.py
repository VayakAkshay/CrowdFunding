from django.shortcuts import render
from .models import Room
from django.contrib.auth.models import User
# Create your views here.

def rooms(request):
    try:
        room = Room.objects.all()
        user = request.user
        user_name = User.objects.get(username = user).first_name
        return render(request,"room/rooms.html",{"username":user_name,"rooms":room}) 
    except:
        return render(request,"room/rooms.html")

def room(request,slug):
    try:
        room = Room.objects.get(slug=slug)
        user = request.user
        user_name = User.objects.get(username = user).first_name
        return render(request,"room/room.html",{"username":user_name,"room":room}) 
    except:
        return render(request,"room/room.html")
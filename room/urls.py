from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.rooms,name="rooms"),
    path('<slug:slug>/',views.room,name="room")
]
from django.contrib import admin
from django.urls import path,include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('Homepage.urls')),
    path('',include('Loginsystem.urls')),
    path('rooms/',include('room.urls')),
]
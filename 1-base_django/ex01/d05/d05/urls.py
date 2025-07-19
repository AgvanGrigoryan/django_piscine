from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('ex01/', include("ex01.urls")),
    path('admin/', admin.site.urls),
]

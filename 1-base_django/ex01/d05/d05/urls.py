from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('ex00/', include("ex00.urls")),
    path('ex01/', include("ex01.urls")),
    path('admin/', admin.site.urls),
]

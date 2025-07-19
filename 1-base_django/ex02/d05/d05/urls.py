from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('ex02/', include("ex02.urls")),
    path('admin/', admin.site.urls),
]

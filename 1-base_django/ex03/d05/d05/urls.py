from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('ex03/', include("ex03.urls")),
    path('admin/', admin.site.urls),
]

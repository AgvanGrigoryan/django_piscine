from django.urls import path
from . import views

urlpatterns = [
    path('display/', views.display, name="display_movie_09"),
]
from django.urls import path
from . import views

urlpatterns = [
    path('init/', views.init),
    path('populate/', views.populate),
    path('display/', views.display, name="display_movie_07"),
]
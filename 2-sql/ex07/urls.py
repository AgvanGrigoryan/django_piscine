from django.urls import path
from . import views

urlpatterns = [
    path('populate/', views.populate),
    path('display/', views.display, name="display_movie_07"),
    path('update/', views.update, name="update_movie_07"),
]
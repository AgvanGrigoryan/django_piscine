from django.urls import path
from . import views

urlpatterns = [
    path('django/', views.Render_ex01_django, name="django"),
    path('display/', views.Render_ex01_display, name="display"),
    path('templates/', views.Render_ex01_templates, name="templates"),
]
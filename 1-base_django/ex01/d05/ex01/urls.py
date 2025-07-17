from django.urls import path
from . import views

urlpatterns = [
    path('django/', views.Render_ex01_django),
    path('display/', views.Render_ex01_display),
    path('templates/', views.Render_ex01_templates),
]
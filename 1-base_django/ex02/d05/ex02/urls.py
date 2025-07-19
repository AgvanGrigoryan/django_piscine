from django.urls import path
from . import views

urlpatterns = [
    path('', views.renderForm, name="main_page"),
    path('add_history/', views.addNewHistory, name="add_history")
]
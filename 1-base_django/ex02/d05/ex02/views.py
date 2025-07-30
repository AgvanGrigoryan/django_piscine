from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse
from django.conf import settings
from .forms import TextForm
from datetime import datetime
import os

def renderForm(request):

    if request.method == "POST":
        return HttpResponse("POST METHOD DOESN'T ALLOW")
    
    form = TextForm()
    history = []
    if os.path.exists(settings.EX02_LOG_PATH):
        with open(settings.EX02_LOG_PATH, mode="r") as logs:
            history = logs.readlines()
    return render(request, "ex02_index.html", {"form": form, "history": history})

def save_logs(log_text: str):
    with open(settings.EX02_LOG_PATH, mode="a") as logs:
        print(f"\033[0;32m{log_text}\033[0m")
        logs.write(f"{log_text}\n")

def addNewHistory(request):
    form = TextForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        save_logs(f"{datetime.now()} - {form.cleaned_data['user_input']}")
        return redirect("main_page")
    return HttpResponse("Invalid values of form")
        

from django.shortcuts import render, HttpResponse

def index(request):
    return render(request, "ex00/index.html")

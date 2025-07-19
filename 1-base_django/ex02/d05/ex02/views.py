from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from  .forms import historyForm

def renderForm(request):

    if request.method == "POST":
        return HttpResponse("POST METHOD DOESN'T ALLOW")
    else:
        form = historyForm()

    return render(request, "main_page.html", {"form": form})

def addNewHistory(request):
    if request.method == "POST":
        form = historyForm(request.POST)
        if form.is_valid():
            return HttpResponse("CONGRATULATIONS BRO!")
    else:
        return HttpResponseRedirect(reverse("main_page"))

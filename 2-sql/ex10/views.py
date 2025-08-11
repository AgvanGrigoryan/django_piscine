from django.shortcuts import render
from .forms import SearchField

def index(request):
    context = dict()
    form = SearchField(request.GET or None)

    context['error_msg'] = "NOT VALID!"
    if form.is_valid():
        is_first_request = False
        context['error_msg'] = "IS VALID"

    context['form'] = form
    context['is_first_request'] = True
    if request.GET:
        context['is_first_request'] = False
    return render(request, 'ex10/search_info.html', context)


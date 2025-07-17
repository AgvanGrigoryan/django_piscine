from django.shortcuts import render

def Render_ex01_django(request):
    return render(request, "ex01/ex01_django.html")

def Render_ex01_display(request):
    return render(request, "ex01/ex01_display.html")

def Render_ex01_templates(request):
    return render(request, "ex01/ex01_templates.html")
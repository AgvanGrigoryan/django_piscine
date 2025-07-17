from django.urls import path

urlpatterns = [
    path('django/', some_django_view),
    path('display/', some_display_view),
    path('templates/', some_templates_view),
]
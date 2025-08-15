from .views import get_display_username

def temp_username_processor(request):
    return {'username': get_display_username(request)}
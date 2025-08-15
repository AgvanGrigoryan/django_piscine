from .views import process_temp_username

def temp_username_processor(request):
    username = process_temp_username(request.session)
    return {'username': username}
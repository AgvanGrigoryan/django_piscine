from django.shortcuts import redirect
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from .forms import RegisterForm

User = get_user_model()

class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

class UserRegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('login-view')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home-view')
        return super().dispatch(request, *args, **kwargs)

class UserLogoutView(LogoutView):
    pass
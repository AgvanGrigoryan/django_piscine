from django.urls import path
from accounts.views import UserRegisterView, UserLoginView, UserLogoutView
urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register-view'),
    path('login/', UserLoginView.as_view(), name='login-view'),
    path('logout/', UserLogoutView.as_view(), name='logout-view'),
]
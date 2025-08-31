from django.urls import path
from .views import HomeView, ArticleListView, UserLoginView

urlpatterns = [
    path('', HomeView.as_view(), name='homeView'),
    path('articles/', ArticleListView.as_view(), name='article-list'),
    path('login/', UserLoginView.as_view(), name='login-view')
]

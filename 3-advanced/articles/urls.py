from django.urls import path
from .views import HomeView, ArticleListView, UserLoginView, UserLogoutView, ArticleDetailView, MyArticleListView, FavouritesListView

urlpatterns = [
    path('', ArticleListView.as_view(), name='article-list'),
    path('<int:pk>/detail/', ArticleDetailView.as_view(), name='article-detail'),
    path('mine/', MyArticleListView.as_view(), name='my-articles'),
    path('favourites/', FavouritesListView.as_view(), name='favourites'),

    path('login/', UserLoginView.as_view(), name='login-view'),
    path('logout/', UserLogoutView.as_view(), name='logout-view'),
]


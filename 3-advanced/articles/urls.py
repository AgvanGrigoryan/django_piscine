from django.urls import path
from .views import HomeView, ArticleListView, ArticleDetailView, MyArticleListView, FavouritesListView, PublishArticleView, AddFavouriteView

urlpatterns = [
    path('', ArticleListView.as_view(), name='article-list'),
    path('<int:pk>/detail/', ArticleDetailView.as_view(), name='article-detail'),
    path('mine/', MyArticleListView.as_view(), name='my-articles'),
    path('favourites/', FavouritesListView.as_view(), name='favourites'),
    path('publish/', PublishArticleView.as_view(), name='publish'),
    path('<int:pk>/add_favourite/', AddFavouriteView.as_view(), name='add-favourite'),
]


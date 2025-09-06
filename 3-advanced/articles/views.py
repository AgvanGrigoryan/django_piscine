from django.shortcuts import render, HttpResponse
from django.views.generic import RedirectView, ListView, DetailView, CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Article, UserFavouriteArticle
from .forms import PublishForm

class HomeView(RedirectView):
    pattern_name = 'article-list'
    permanent = False

class ArticleListView(ListView):
    model = Article
    template_name = 'articles/article_list.html'
    context_object_name = 'articles'
    # paginate_by = 10

class MyArticleListView(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'articles/my_article_list.html'
    context_object_name = 'articles'
    redirect_field_name = 'next'
    # paginate_by = 10

    def get_queryset(self):
        return (
            Article.objects
            .filter(author=self.request.user)
            .select_related('author')
        )

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'articles/article_detail.html'
    context_object_name = 'article'

class FavouritesListView(LoginRequiredMixin, ListView):
    model = UserFavouriteArticle
    template_name = 'articles/favourite_articles.html'
    context_object_name = 'articles'
    redirect_field_name = 'next'

    def get_queryset(self):
        return (
            Article.objects
            .filter(favourited_by__user=self.request.user)
            .select_related('author')
        )

class PublishArticleView(LoginRequiredMixin, CreateView):
    model = Article
    form_class = PublishForm
    redirect_field_name = 'next'
    template_name = 'articles/publish_article.html'
    success_url = reverse_lazy('article-list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

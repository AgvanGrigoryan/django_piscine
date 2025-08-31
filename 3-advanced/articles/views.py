from django.shortcuts import render
from django.views.generic import RedirectView, ListView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .models import Article

class HomeView(RedirectView):
    pattern_name = 'article-list'
    permanent = False

class ArticleListView(ListView):
    model = Article
    template_name = 'articles/article_list.html'
    context_object_name = 'articles'
    # paginate_by = 10

class UserLoginView(LoginView):
    template_name = 'articles/login.html'
    redirect_authenticated_user = True
    next_page = reverse_lazy('home')
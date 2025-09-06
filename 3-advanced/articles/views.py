from django.shortcuts import render, HttpResponse, redirect
from django.views.generic import RedirectView, ListView, DetailView, CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Article, UserFavouriteArticle
from .forms import PublishForm, AddFavouriteForm

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['add_favourite_form'] = AddFavouriteForm(initial={'article': self.object.pk})
            context['already_favourite'] = UserFavouriteArticle.objects.filter(
                user=self.request.user, article=self.object
            ).exists()
        else:
            context['add_favourite_form'] = None
            context['already_favourite'] = False
        return context

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
    success_url = reverse_lazy('my-articles')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class AddFavouriteView(LoginRequiredMixin, CreateView):
    model = UserFavouriteArticle
    form_class = AddFavouriteForm
    redirect_field_name = 'next'
    template_name = 'articles/add_favourite.html'

    # def get_form(self, form_class=None):
    #     form = super().get_form(form_class)
    #     form.fields['article'].initial = self.kwargs['pk']
    #     print(">>> Initial data: ", form)
    #     return form
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        if UserFavouriteArticle.objects.filter(user=self.request.user, article=form.instance.article).exists():
            return redirect('article-detail', pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['article'] = Article.objects.get(pk=self.kwargs['pk'])
        return context
    
    def get_success_url(self):
        return reverse_lazy('article-detail', kwargs={'pk': self.kwargs['pk']})

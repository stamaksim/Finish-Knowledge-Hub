from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from django.views import generic
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from knowhub.models import Articles, Category


def home(request):
    context = {
        "articles": Articles.objects.all()
    }
    return render(request, "knowhub/home.html", context)


class ArticleListView(ListView):
    model = Articles
    template_name = "knowhub/home.html"
    context_object_name = "articles"
    ordering = ["-creation_date"]


class ArticleDetailView(DetailView):
    model = Articles


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Articles
    fields = ["name", "description", "category"]

    def form_valid(self, form):
        form.instance.user = self.request.user
        category = form.cleaned_data["category"]
        article = form.save(commit=False)
        article.category = category
        article.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("article-detail", kwargs={"pk": self.object.pk})


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Articles
    fields = ["category", "description", "name"]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        article = self.get_object()
        if self.request.user == article.user:
            return True
        return False


class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Articles
    success_url = "/"

    def test_func(self):
        article = self.get_object()
        if self.request.user == article.user:
            return True
        return False

class CategoryListView(LoginRequiredMixin, generic.ListView):
    model = Category
    context_object_name = "category_list"
    template_name = "knowhub/category_list.html"


class CategoryDetailView(LoginRequiredMixin, DetailView):
    model = Category
    template_name = "knowhub/category_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.object
        articles = Articles.objects.filter(category=category)
        context["article_list"] = articles
        return context



def about(request):
    return render(request, "knowhub/about.html", {"title": "About something"})

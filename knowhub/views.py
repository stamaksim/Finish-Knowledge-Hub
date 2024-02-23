from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from knowhub.models import Articles


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
    fields = ["category", "name", "description"]


    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


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



def about(request):
    return render(request, "knowhub/about.html", {"title": "About something"})

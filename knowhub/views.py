from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic.edit import FormMixin
from knowhub.forms import CommentForm, ArticlesSearchForm, ServiceSearchForm
from knowhub.models import Articles, Category, Comment, Services
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)


def home(request):
    context = {"articles": Articles.objects.all()}
    return render(request, "knowhub/home.html", context)


class ArticleListView(LoginRequiredMixin, ListView):
    model = Articles
    template_name = "knowhub/home.html"
    context_object_name = "articles"
    ordering = ["-creation_date"]


class ArticleDetailView(LoginRequiredMixin, DetailView, FormMixin):
    model = Articles
    template_name = "knowhub/articles_detail.html"
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comment_form"] = CommentForm()
        return context


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Articles
    fields = ["name", "description", "category", "text"]

    def form_valid(self, form):
        form.instance.user = self.request.user
        category = form.cleaned_data["category"]
        article = form.save(commit=False)
        article.category = category
        article.save()
        self.object = article
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
        category = self.get_object()
        articles = Articles.objects.filter(category=category)
        if self.request.GET.get("title"):
            articles = articles.filter(name__icontains=self.request.GET.get("title"))
        paginator = Paginator(articles, 3)

        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context["article_list"] = page_obj
        title = self.request.GET.get("title", "")
        context["search_form"] = ArticlesSearchForm(initial={"title": title})
        return context


class CommentCreateView(CreateView):
    model = Comment
    fields = ("text",)
    template_name = "knowhub/comment.html"

    def get_success_url(self):
        return self.object.article.get_absolute_url()

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.article = get_object_or_404(Articles, pk=self.kwargs["pk"])
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pk"] = self.kwargs["pk"]
        return context


class CommentDetailView(DetailView):
    model = Comment
    template_name = "knowhub/comment_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comment"] = self.object
        return context


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    fields = ["text"]
    template_name = "knowhub/comment_update.html"

    def get_success_url(self):
        return reverse_lazy("article-detail", kwargs={"pk": self.object.article.pk})

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = "knowhub/comment_confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy("article-detail", kwargs={"pk": self.object.article.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comment"] = self.object
        return context


class ServicesListView(LoginRequiredMixin, ListView):
    model = Services
    context_object_name = "services_list"
    template_name = "knowhub/services_list.html"
    paginate_by = 5

    def get_queryset(self):
        form = ServiceSearchForm(self.request.GET)
        if form.is_valid():
            return Services.objects.filter(name__icontains=form.cleaned_data["title"])

        return Services.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ServicesListView, self).get_context_data(**kwargs)
        title = self.request.GET.get("title", "")
        context["search_form"] = ServiceSearchForm(initial={"title": title})
        return context


class ServicesDetailView(LoginRequiredMixin, DetailView):
    model = Services
    template_name = "knowhub/services_detail.html"


class ServicesCreateView(LoginRequiredMixin, CreateView):
    model = Services
    template_name = "knowhub/services_create.html"
    fields = ["name", "description", "price", "content"]

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("services-detail", kwargs={"pk": self.object.pk})


class ServicesUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Services
    fields = ["category", "description", "name"]
    template_name = "knowhub/services_update.html"
    success_url = reverse_lazy("services-list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def test_func(self):
        serv = self.get_object()
        if self.request.user == serv.owner:
            return True
        return False


class ServicesDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Services
    success_url = "/"

    def test_func(self):
        serw = self.get_object()
        if self.request.user == serw.owner:
            return True
        return False


def about(request):
    return render(request, "knowhub/about.html", {"title": "About something"})

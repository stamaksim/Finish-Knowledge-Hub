from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from django.views import generic, View
from django.views.generic.edit import FormMixin
from knowhub.forms import CommentForm, ArticlesSearchForm, ServiceSearchForm
from django.contrib import messages
from knowhub.models import Articles, Category, Comment, Services
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)


@login_required
def home(request):
    # context = {"articles": Articles.objects.all()}
    return render(request, "knowhub/home.html")


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
    fields = ["category", "description", "name", "text"]

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
    slug_url_kwarg = "category_slug"
    slug_field = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.get_object()
        articles = Articles.objects.filter(category=category)
        if self.request.GET.get("title"):
            articles = articles.filter(name__icontains=self.request.GET.get("title"))
        paginator = Paginator(articles, 6)

        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context["article_list"] = page_obj
        title = self.request.GET.get("title", "")
        context["search_form"] = ArticlesSearchForm(initial={"title": title})
        return context


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ("text",)
    template_name = "knowhub/comment.html"

    def get_success_url(self):
        return reverse("all-comments", kwargs={"pk": self.kwargs["pk"]})

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.article = get_object_or_404(Articles, pk=self.kwargs["pk"])
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pk"] = self.kwargs["pk"]
        return context


class CommentDetailView(LoginRequiredMixin, DetailView):
    model = Comment
    template_name = "knowhub/comment_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comment"] = self.object
        context["author"] = self.object.author
        return context


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    fields = ["text"]
    template_name = "knowhub/comment_update.html"

    def get_success_url(self):
        return reverse_lazy("all-comments", kwargs={"pk": self.object.article.pk})

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.author != request.user:
            messages.error(request, "You are not authorized to edit this comment")
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = "knowhub/comment_confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy("all-comments", kwargs={"pk": self.object.article.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comment"] = self.object
        return context

    def dispatch(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.author != request.user:
            messages.error(request, "You are not authorized to delete this comment")
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


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


class SearchView(View):
    def get(self, request):
        search_type = request.GET.get("search_type")
        search_query = request.GET.get("query")

        if search_query:
            articles = Articles.objects.filter(name__icontains=search_query)
            services = Services.objects.filter(name__icontains=search_query)

            if search_type == "articles":
                results = articles
            elif search_type == "services":
                results = services
            else:
                results = list(articles) + list(services)
        else:
            articles = Articles.objects.all()
            services = Services.objects.all()
            results = list(articles) + list(services)

        context = {
            "results": results,
            "search_query": search_query,
            "search_type": search_type,
        }
        return render(request, "knowhub/search_results.html", context)


class AllCommentsView(LoginRequiredMixin, ListView):
    template_name = "knowhub/all_comments.html"
    context_object_name = "comments"

    def get_queryset(self):
        article_id = self.kwargs.get("pk")
        return Comment.objects.filter(article_id=article_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = get_object_or_404(Articles, pk=self.kwargs.get("pk"))
        context["article"] = article
        context["form"] = CommentForm()
        return context


def about(request):
    return render(
        request,
        "includes/about.html",
        {"title": "About something", "is_about_page": True},
    )

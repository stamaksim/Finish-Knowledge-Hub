from django.urls import path
from .views import (
    ArticleListView,
    ArticleDetailView,
    ArticleCreateView,
    ArticleUpdateView,
    ArticleDeleteView,
    CategoryDetailView,
    CategoryListView,
    CommentCreateView,
    CommentUpdateView,
    CommentDeleteView

)
from knowhub import views

urlpatterns = [
    path('', ArticleListView.as_view(), name="knowhub-home"),
    path("about/", views.about, name="knowhub-about"),
    path("article/<int:pk>/", ArticleDetailView.as_view(), name="article-detail"),
    path("article/new/", ArticleCreateView.as_view(), name="article-create"),
    path("article/<int:pk>/update/", ArticleUpdateView.as_view(), name="article-update"),
    path("article/<int:pk>/delete/", ArticleDeleteView.as_view(), name="article-delete"),
    path("categories/",CategoryListView.as_view(),name="category-list"),
    path("categories/<int:pk>/", CategoryDetailView.as_view(), name="category-detail"),
    path("article/<int:pk>/comment/", CommentCreateView.as_view(), name="comment-create"),
    path("comment/<int:pk>/update", CommentUpdateView.as_view(), name="comment-update"),
    path("comment/<int:pk>/delete", CommentDeleteView.as_view(), name="comment-delete"),

]
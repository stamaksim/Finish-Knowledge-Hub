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
    CommentDeleteView,
    ServicesListView,
    ServicesCreateView,
    ServicesDetailView,
    ServicesUpdateView,
    ServicesDeleteView,
)
from knowhub import views

urlpatterns = [
    path("", ArticleListView.as_view(), name="knowhub-home"),
    path("about/", views.about, name="knowhub-about"),
    path("article/<int:pk>/", ArticleDetailView.as_view(), name="article-detail"),
    path("article/new/", ArticleCreateView.as_view(), name="article-create"),
    path(
        "article/<int:pk>/update/", ArticleUpdateView.as_view(), name="article-update"
    ),
    path(
        "article/<int:pk>/delete/", ArticleDeleteView.as_view(), name="article-delete"
    ),
    path(
        "article/<int:pk>/comment/", CommentCreateView.as_view(), name="comment-create"
    ),
    path("categories/", CategoryListView.as_view(), name="category-list"),
    path("categories/<int:pk>/", CategoryDetailView.as_view(), name="category-detail"),
    path("comment/<int:pk>/update", CommentUpdateView.as_view(), name="comment-update"),
    path("comment/<int:pk>/delete", CommentDeleteView.as_view(), name="comment-delete"),
    path("services/", ServicesListView.as_view(), name="services-list"),
    path("services/create/", ServicesCreateView.as_view(), name="services-create"),
    path("services/<int:pk>/", ServicesDetailView.as_view(), name="services-detail"),
    path(
        "services/<int:pk>/update/",
        ServicesUpdateView.as_view(),
        name="services-update",
    ),
    path(
        "services/<int:pk>/delete/",
        ServicesDeleteView.as_view(),
        name="services-delete",
    ),
]

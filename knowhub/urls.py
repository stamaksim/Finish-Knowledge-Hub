from django.urls import path

from knowhub import views

urlpatterns = [
    path('', views.home, name="knowhub-home"),
    path("about/", views.about, name="knowhub-about")
]
from django.shortcuts import render
from knowhub.models import Category


def home(request):
    context = {
        "categories": Category.objects.all()
    }
    return render(request, "knowhub/home.html", context)


def about(request):
    return render(request, "knowhub/about.html", {"title": "About something"})

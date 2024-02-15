from django.shortcuts import render


posts = [
    {
        "author": "MaksST",
        "title": "Blog 1",
        "content": "First post content",
        "date_posted": "February 14, 2024"
    },
    {
        "author": "RaminaST",
        "title": "Blog 2",
        "content": "Second post content",
        "date_posted": "February 15, 2024"
    }
]


def home(request):
    context = {
        "posts": posts
    }
    return render(request, "knowhub/home.html", context)


def about(request):
    return render(request, "knowhub/about.html", {"title": "About something"})

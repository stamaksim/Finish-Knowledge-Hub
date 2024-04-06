from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify


class User(AbstractUser):
    class Meta:
        ordering = ("username",)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="category name")
    slug = models.SlugField(max_length=100, unique=True)
    description = models.CharField(max_length=255)
    creation = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ("creation",)

    def save(self, *args, **kwargs):
        if not self.slug:

            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"


class Articles(models.Model):
    name = models.CharField(max_length=65)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="categories_articles"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="articles_users",
    )
    description = models.CharField(max_length=255)
    text = models.TextField()
    creation_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.category}: ({self.name}{self.description})"

    def get_absolute_url(self):
        return reverse("article-detail", kwargs={"pk": self.pk})


class Services(models.Model):
    name = models.CharField(max_length=65)
    description = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=5, decimal_places=2, blank=True)
    content = models.TextField()
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="services",
    )

    def __str__(self):
        return (
            f"{self.name}: ({self.description}{self.category}{self.price}{self.owner})"
        )


class Comment(models.Model):
    text = models.TextField(max_length=300)
    date = models.DateTimeField(default=timezone.now)
    article = models.ForeignKey(
        Articles, on_delete=models.CASCADE, related_name="comments"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments_authors",
    )

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return self.text

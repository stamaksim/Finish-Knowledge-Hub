from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from knowhub.models import Articles, Category, User, Comment, Services

ARTICLES_URL = reverse("knowhub-home")
CATEGORY_URL = reverse("category-list")
SERVICES_URL = reverse("services-list")


class PublicArticlesTest(TestCase):
    def test_login_required(self):
        res = self.client.get(ARTICLES_URL)
        self.assertNotEquals(res.status_code, 200)


class PrivateArticlesTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create(
            username="test username", password="test123"
        )
        self.client.force_login(self.user)
        self.category = Category.objects.create(name="Test Name")

    def test_retrieve_articles(self):
        Articles.objects.create(
            name="TestArticle",
            description="Test description",
            category=self.category,
            text="Test text",
            user=self.user,
        )
        response = self.client.get(ARTICLES_URL)
        self.assertEqual(response.status_code, 200)
        articles = Articles.objects.all()
        self.assertEqual(list(response.context["articles"]), list(articles))
        self.assertTemplateUsed(response, template_name="knowhub/home.html")


class PublicCategoryTest(TestCase):
    def test_login_required(self):
        res = self.client.get(CATEGORY_URL)
        self.assertNotEquals(res.status_code, 200)


class PrivateCategoryTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test username", password="test123"
        )
        self.client.force_login(self.user)
        self.category = Category.objects.create(name="Test Name")

        response = self.client.get(CATEGORY_URL)
        self.assertEqual(response.status_code, 200)
        categories = Category.objects.all()
        self.assertEqual(
            list(response.context["categories"]), list(categories)
        )
        self.assertTemplateUsed(
            response, template_name="knowhub/category_list.html"
        )


class ServicesCategoryTest(TestCase):
    def test_login_required(self):
        res = self.client.get(SERVICES_URL)
        self.assertNotEquals(res.status_code, 200)


class PrivateServicesTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test username", password="test123"
        )
        self.client.force_login(self.user)
        self.services = Services.objects.create(name="Test Name")

        response = self.client.get(SERVICES_URL)
        self.assertEqual(response.status_code, 200)
        services = Services.objects.all()
        self.assertEqual(list(response.context["services"]), list(services))
        self.assertTemplateUsed(
            response, template_name="knowhub/services_list.html"
        )

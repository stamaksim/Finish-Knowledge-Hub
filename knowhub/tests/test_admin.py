from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from knowhub.models import Services, Category, Articles


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin", password="testadmin"
        )

        self.client.force_login(self.admin_user)
        self.service = Services.objects.create(
            name="Test Service",
            description="Test Description",
            category="Test Category",
            price=100,
            content="Test Content",
            owner=self.admin_user,
        )
        self.category = Category.objects.create(
            name="Test Category", description="Test Description"
        )
        self.article = Articles.objects.create(
            name="Test Name",
            category=self.category,
            description="Test Description",
            user=self.admin_user,
        )

    def test_services_listed(self):
        """Test that services are listed on services page"""
        url = reverse("admin:knowhub_services_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.service.name)
        self.assertContains(response, self.service.description)
        self.assertContains(response, self.service.category)
        self.assertContains(response, self.service.price)

    def test_service_edit_page(self):
        """Test that the service edit page works"""
        url = reverse("admin:knowhub_services_change", args=[self.service.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_services_create_page(self):
        """Test that the services create page work"""
        url = reverse("admin:knowhub_services_add")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_services_delete_page(self):
        """Test that the service delete page works"""
        url = reverse("admin:knowhub_services_delete", args=[self.service.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_category_listed(self):
        """Test that categories are listed on category page"""
        url = reverse("admin:knowhub_category_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.category.name)
        self.assertContains(response, self.category.description)

    def test_category_edit_page(self):
        """Test that the category edit page works"""
        url = reverse("admin:knowhub_category_change", args=[self.category.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_category_delete_page(self):
        """Test that the category delete page works"""
        url = reverse("admin:knowhub_category_delete", args=[self.category.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_article_listed(self):
        """Test that articles are listed on  page"""
        url = reverse("admin:knowhub_articles_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.article.name)
        self.assertContains(response, self.article.category)
        self.assertContains(response, self.article.description)

    def test_article_edit_page(self):
        """Test that the articles edit page works"""
        url = reverse("admin:knowhub_articles_change", args=[self.article.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_article_delete_page(self):
        """Test that the articles delete page works"""
        url = reverse("admin:knowhub_articles_delete", args=[self.article.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

from django.contrib.auth import get_user_model
from django.test import TestCase

from knowhub.models import Category, Articles, Services, Comment


class ModelsTests(TestCase):
    def test_category_format_str(self):
        category = Category.objects.create(name="test")
        self.assertEqual(str(category), category.name)

    def test_user_str(self):
        user = get_user_model().objects.create(
            first_name="test", last_name="test_last", password="test12345"
        )
        full_name = f"{user.first_name} {user.last_name}"
        self.assertEqual(str(user), full_name)

    def test_articles_str(self):
        category = Category.objects.create(name="test")
        user = get_user_model().objects.create(
            first_name="test", last_name="test_last", password="test12345"
        )
        article = Articles.objects.create(
            name="test",
            category=category,
            user=user,
            description="test_description",
            text="lorem_text",
        )
        self.assertEqual(
            str(article),
            f"{article.category}:" f" ({article.name}{article.description})",
        )

    def test_services_str(self):
        user = get_user_model().objects.create(
            first_name="test", last_name="test_last", password="test12345"
        )
        service = Services.objects.create(
            name="test_name",
            description="test_description",
            category="test_category",
            price=100,
            owner=user,
        )
        self.assertEqual(
            str(service),
            f"{service.name}:"
            f" ("
            f"{service.description}"
            f"{service.category}"
            f"{service.price}"
            f"{service.owner}"
            f")",
        )

    def test_comment_str(self):
        user = get_user_model().objects.create(
            first_name="test", last_name="test_last", password="test12345"
        )
        category = Category.objects.create(name="test")

        article = Articles.objects.create(
            name="test",
            category=category,
            user=user,
            description="test_description",
            text="lorem_text",
        )
        comment = Comment.objects.create(
            text="lorem_text", author=user, article=article
        )

        self.assertEqual(str(comment), comment.text)


class UserCreateTest(TestCase):
    def test_user_create(self):
        username = "test"
        first_name = "test"
        last_name = "test_last"
        password = "test12345"
        user = get_user_model().objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )

        self.assertEqual(user.username, username)
        self.assertEqual(user.first_name, first_name)
        self.assertEqual(user.last_name, last_name)
        self.assertTrue(user.check_password(password))

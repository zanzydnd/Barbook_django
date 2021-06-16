from django.contrib.auth.models import AnonymousUser
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, RequestFactory

from barbook_app.models import BarbookUser
from barbook_app.views import CreateCocktail


class BarbookViewsTestCases(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()
        image = SimpleUploadedFile(
            name="avatar.jpg", content=b"", content_type="image/jpg"
        )
        self.user = BarbookUser.objects.create(
            name="Тестер",
            email="test@mail.ru",
            second_name="Тестев",
            username="tester",
            img=image,
        )

    def test_create_cocktail_unauthorized_view(self):
        request = self.factory.get("")
        request.user = AnonymousUser()
        response = CreateCocktail.as_view()(request)
        self.assertEqual(response.status_code, 302)

    def test_create_cocktail_view(self):
        request = self.factory.get("")
        request.user = self.user
        response = CreateCocktail.as_view()(request)
        self.assertEqual(response.status_code, 200)

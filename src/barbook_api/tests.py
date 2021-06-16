import io
import json
import pprint

from PIL import Image
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import QueryDict
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
import mock

from barbook_app.models import Cocktail, BarbookUser, Ingredient, BarTool


class ApiTests(APITestCase):
    def setUp(self):
        user_test1 = BarbookUser.objects.create(
            id=1,
            name="danya",
            username="danya",
            email="albert@mail.ru",
            password="123123",
        )
        user_test1.save()

        user_test2 = BarbookUser.objects.create(
            id=2,
            name="ne danya",
            username="ne_danya",
            email="ne_albert@mail.ru",
            password="ne_123123",
        )
        user_test2.save()

        img_mock = mock.MagicMock(spec=File)
        img_mock.name = "default.jpg"

        ing1 = Ingredient.objects.create(
            id=1,
            name="ingredient1",
            description="description1",
            img=img_mock.name,
            small_img=img_mock.name,
        )
        ing2 = Ingredient.objects.create(
            id=2,
            name="ingredient2",
            description="description2",
            img=img_mock.name,
            small_img=img_mock.name,
        )
        ing3 = Ingredient.objects.create(
            id=3,
            name="ingredient3",
            description="description3",
            img=img_mock.name,
            small_img=img_mock.name,
        )
        tool1 = BarTool.objects.create(
            id=1,
            name="tool1",
            description="descrp1",
            img=img_mock.name,
            small_img=img_mock.name,
        )
        tool2 = BarTool.objects.create(
            id=2,
            name="tool2",
            description="descrp2",
            img=img_mock.name,
            small_img=img_mock.name,
        )
        tool3 = BarTool.objects.create(
            id=3,
            name="tool3",
            description="descrp3",
            img=img_mock.name,
            small_img=img_mock.name,
        )

        cocktail = Cocktail.objects.create(
            id=1, name="Test", description="Testable", recipe_text={"1": "1", "2": "2"}
        )

    def test_unauthorized_get_list_ingredient(self):
        response = self.client.get(reverse("ingredient-list"))  # "/api/ingredients/"
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_list_ingredient(self):
        user = BarbookUser.objects.get(id=1)
        self.client.force_login(user=user)
        response = self.client.get(reverse("ingredient-list"))  # "/api/ingredients/"
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_fail_ingredient_object(self):
        user = BarbookUser.objects.get(id=1)
        self.client.force_login(user=user)
        response = self.client.get(
            reverse("ingredient-detail", kwargs={"pk": 5})
        )  # "/api/ingredients/5/"
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_ingredient_object(self):
        user = BarbookUser.objects.get(id=1)
        self.client.force_login(user=user)
        response = self.client.get(
            reverse("ingredient-detail", kwargs={"pk": 2})
        )  # "/api/ingredients/2/"
        self.assertEqual(response.data["id"], 2)
        self.assertEqual(response.data["name"], "ingredient2")

    def test_fail_delete_cocktail(self):
        user = BarbookUser.objects.get(id=1)
        self.client.force_login(user=user)
        response = self.client.delete(
            reverse("cocktail_-detail", kwargs={"pk": 2})
        )  # "/api/cocktails/2/"
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_cocktail(self):
        user = BarbookUser.objects.get(id=1)
        self.client.force_login(user=user)
        response = self.client.delete(
            reverse("cocktail_-detail", kwargs={"pk": 1})
        )  # "/api/cocktails/1/"
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_fail_put_cocktail(self):
        user = BarbookUser.objects.get(id=1)
        self.client.force_login(user=user)
        data_without_name = {"description": "new_description"}
        response = self.client.put(
            reverse("cocktail_-detail", kwargs={"pk": 1}),
            data=json.dumps(data_without_name),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data_without_descriprion = {"name": "new_name"}
        response = self.client.put(
            reverse("cocktail_-detail", kwargs={"pk": 1}),
            data=json.dumps(data_without_descriprion),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_cocktail(self):
        user = BarbookUser.objects.get(id=2)
        self.client.force_login(user=user)
        data = {"name": "new_name", "description": "new_descrp"}
        response = self.client.put(
            reverse("cocktail_-detail", kwargs={"pk": 1}),
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated = Cocktail.objects.get(id=1)
        self.assertEqual(response.data["name"], "new_name")
        self.assertEqual(updated.name, "new_name")
        self.assertEqual(updated.description, "new_descrp")

    def test_unauthenticated_create_cocktail(self):
        response = self.client.post(reverse("cocktail_create"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_bad_request_create_cocktail(self):
        user = BarbookUser.objects.get(id=1)
        self.client.force_login(user=user)
        data = {
            "author": "3",
            "name": "Fail_test",
            "description": "description_fail_test",
            "recipe_text": {"1": "asd", "2": "asd"},
            "recipe": [{"ingredient": 1, "amount": 1}, {"ingredient": 2, "amount": 2}],
            "cocktail_tool": [{"tool": 1, "amount": 1}, {"tool": 2, "amount": 2}],
        }
        response = self.client.post(
            reverse("cocktail_create"), data=data, content_type="multipart/form-data"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_cocktail(self):
        user = BarbookUser.objects.get(id=1)
        self.client.force_login(user=user)

        image = io.BytesIO()
        Image.new("RGB", (150, 150)).save(image, "JPEG")
        image.seek(0)
        file_uploaded = SimpleUploadedFile("image.jpg", image.getvalue())
        file_uploaded2 = SimpleUploadedFile("image.jpg", image.getvalue())
        data = {
            "author": "1",
            "name": "success_test",
            "description": "description_success_test",
            "recipe_text": '{"1": "asd", "2": "asd"}',
            "recipe[0]ingredient": "1",
            "recipe[0]amount": "1",
            "recipe[1]ingredient": "2",
            "recipe[1]amount": "2",
            "cocktail_tool[0]tool": "1",
            "cocktail_tool[0]amount": "1",
            "cocktail_tool[1]tool": "2",
            "cocktail_tool[1]amount": "2",
            "img": file_uploaded,
            "small_img": file_uploaded2,
        }
        response = self.client.post(reverse("cocktail_create"), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

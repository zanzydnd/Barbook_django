from django.contrib.auth.models import AnonymousUser
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, RequestFactory
from django.test import Client
import mock
from django.urls import reverse

from barbook_app.models import (
    BarbookUser,
    ClassForCocktailTag,
    TagForCocktail,
    Ingredient,
    BarTool,
    Cocktail,
    CocktailRecipe,
)
from barbook_app.models.stuff import CocktailTool
from barbook_app.services import (
    get_tags_and_their_classes_for_cocktail,
    get_cocktails_where_ingredient_is_being_used,
    get_cocktail_prepared,
    favorite,
    search,
    new_like,
    new_comment_service,
    prepare_cocktails_where_ingredient_is_being_used,
)
from barbook_app.views import Cocktails, CreateCocktail


class BarbookServicesTestCases(TestCase):
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

        self.first_class_for_cocktail_tag = ClassForCocktailTag.objects.create(
            class_name="Первый"
        )
        self.second_class_for_cocktail_tag = ClassForCocktailTag.objects.create(
            class_name="Второй"
        )

        self.first_tag = TagForCocktail.objects.create(
            class_name=self.first_class_for_cocktail_tag, tag_name="Тег1"
        )

        self.second_tag = TagForCocktail.objects.create(
            class_name=self.first_class_for_cocktail_tag, tag_name="Тег2"
        )

        self.third_tag = TagForCocktail.objects.create(
            class_name=self.second_class_for_cocktail_tag, tag_name="Тег3"
        )

        self.fourth_tag = TagForCocktail.objects.create(
            class_name=self.second_class_for_cocktail_tag, tag_name="Тег4"
        )

        self.first_ingredient = Ingredient.objects.create(
            name="Ингредиент 1",
            small_img=image,
            img=image,
            description="Первый ингредиент",
        )

        self.second_ingredient = Ingredient.objects.create(
            name="Ингредиент 2",
            small_img=image,
            img=image,
            description="Второй ингредиент",
        )

        self.third_ingredient = Ingredient.objects.create(
            name="Ингредиент 3",
            small_img=image,
            img=image,
            description="Третий ингредиент",
        )

        self.first_tool = BarTool.objects.create(
            name="предмет 1", small_img=image, img=image, description="Первый предмет"
        )

        self.second_tool = BarTool.objects.create(
            name="предмет 2", small_img=image, img=image, description="Второй предмет"
        )

        self.third_tool = BarTool.objects.create(
            name="предмет 3", small_img=image, img=image, description="Третий предмет"
        )

        self.first_cocktail = Cocktail.objects.create(
            name="Первый",
            description="Первый",
            img=image,
            small_img=image,
            author=self.user,
            recipe_text={"1": "Первый", "2": "Второй"},
        )

        self.first_cocktail.cocktail_tag.add(self.first_tag)
        self.first_cocktail.cocktail_tag.add(self.third_tag)

        self.second_cocktail = Cocktail.objects.create(
            name="Второй",
            description="Второй",
            img=image,
            small_img=image,
            author=self.user,
            recipe_text={"1": "Первый", "2": "Второй"},
        )

        self.second_cocktail.cocktail_tag.add(self.second_tag)
        self.second_cocktail.cocktail_tag.add(self.fourth_tag)

        self.third_cocktail = Cocktail.objects.create(
            name="Третий",
            description="Третий",
            img=image,
            small_img=image,
            author=self.user,
            recipe_text={"1": "Первый", "2": "Второй"},
        )

        self.third_cocktail.cocktail_tag.add(self.third_tag)

        CocktailRecipe.objects.create(
            cocktail=self.first_cocktail, ingredient=self.first_ingredient, amount=100
        )

        CocktailRecipe.objects.create(
            cocktail=self.first_cocktail, ingredient=self.second_ingredient, amount=200
        )

        CocktailRecipe.objects.create(
            cocktail=self.second_cocktail, ingredient=self.second_ingredient, amount=200
        )

        CocktailRecipe.objects.create(
            cocktail=self.second_cocktail, ingredient=self.third_ingredient, amount=200
        )

        CocktailRecipe.objects.create(
            cocktail=self.third_cocktail, ingredient=self.first_ingredient, amount=200
        )
        # --------------------------------------------
        CocktailTool.objects.create(
            cocktail=self.first_cocktail, tool=self.first_tool, amount=1
        )

        CocktailTool.objects.create(
            cocktail=self.first_cocktail, tool=self.second_tool, amount=2
        )

        CocktailTool.objects.create(
            cocktail=self.second_cocktail, tool=self.second_tool, amount=1
        )

        CocktailTool.objects.create(
            cocktail=self.second_cocktail, tool=self.third_tool, amount=1
        )

        CocktailTool.objects.create(
            cocktail=self.third_cocktail, tool=self.first_tool, amount=1
        )

    # services

    def test_get_classes_service(self):
        map_ = get_tags_and_their_classes_for_cocktail()
        keys = map_.keys()
        self.assertIn("Первый", keys)
        self.assertIn("Второй", keys)
        self.assertEqual(len(map_.get("Первый")), 2)
        self.assertEqual(len(map_.get("Второй")), 2)

    def test_get_cocktails_by_ingredients(self):
        first_ingred_recipe = get_cocktails_where_ingredient_is_being_used(
            self.first_ingredient
        )
        self.assertEqual(len(first_ingred_recipe), 2)
        self.assertIn(first_ingred_recipe[0].cocktail.name, "Первый")
        self.assertIn(first_ingred_recipe[1].cocktail.name, "Третий")
        second_ingred_recipe = get_cocktails_where_ingredient_is_being_used(
            self.second_ingredient
        )
        self.assertEqual(len(second_ingred_recipe), 2)
        self.assertIn(second_ingred_recipe[0].cocktail.name, "Первый")
        self.assertIn(second_ingred_recipe[1].cocktail.name, "Второй")

    def test_get_cocktail_prepared(self):
        corteg = get_cocktail_prepared(self.first_cocktail)
        self.assertEqual(corteg[0], self.first_cocktail.recipe_text)
        self.assertEqual(corteg[1][0].ingredient.name, "Ингредиент 1")
        self.assertEqual(corteg[1][1].ingredient.name, "Ингредиент 2")
        self.assertEqual(corteg[3], 0)
        self.assertEqual(len(corteg[4]), 0)

    def test_favourite(self):
        favorite(self.first_cocktail.id, self.user)
        self.assertEqual(len(self.user.favourite.all()), 1)
        favorite(self.second_cocktail.id, self.user)
        self.assertEqual(len(self.user.favourite.all()), 2)

    def test_search(self):
        tags = ["Тег1", "Тег2"]
        result = search(tags=tags, search_str="Перв")
        self.assertIn(self.first_cocktail, result)

        result = search(tags=tags, search_str=None)
        self.assertIn(self.first_cocktail, result)
        self.assertIn(self.second_cocktail, result)

        result = search(search_str="Трет", tags=None)
        self.assertIn(self.third_cocktail, result)

    def test_like(self):
        rate = new_like(self.second_cocktail.id, self.user)
        self.assertEqual(rate, 1)
        rate = new_like(self.second_cocktail.id, self.user)
        self.assertEqual(rate, 0)

    def test_comment(self):
        new = new_comment_service("test", self.user.id, self.first_cocktail.id)
        self.assertEqual(new["name"], self.user.name)
        self.assertEqual(new["text"], "test")

        self.assertEqual(len(self.first_cocktail.commentoncocktail_set.all()), 1)

        new_comment_service("test", self.user.id, self.first_cocktail.id)
        self.assertEqual(len(self.first_cocktail.commentoncocktail_set.all()), 2)

    def test_preparation_of_cocktails_by_ingredient(self):
        cockts = prepare_cocktails_where_ingredient_is_being_used(self.first_ingredient)
        keys = cockts.keys()
        self.assertEqual(len(keys), 2)
        self.assertIn(self.first_cocktail, keys)
        self.assertIn(self.third_cocktail, keys)

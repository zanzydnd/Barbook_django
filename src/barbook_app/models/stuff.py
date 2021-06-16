from django.db import models
from .user import BarbookUser
from .base import BaseModel  # , TagBaseModel, ClassForSmthBaseModel
from djchoices import DjangoChoices, ChoiceItem


# cocktail ------------------
class ClassForCocktailTag(models.Model):
    class_name = models.CharField(max_length=255, default="без класса")

    def __str__(self):
        return self.class_name

    class Meta:
        db_table = "class_for_cocktail_tag"
        verbose_name = "Класс для тегов коктейля"
        verbose_name_plural = "Классы для тегов коктейля"


class TagForCocktail(models.Model):
    class_name = models.ForeignKey(
        ClassForCocktailTag,
        on_delete=models.SET_DEFAULT,
        default="без класса",
        related_name="classes",
    )
    tag_name = models.CharField(max_length=255, default="Любые", unique=True)

    def __str__(self):
        return self.tag_name

    class Meta:
        unique_together = (("tag_name", "class_name"),)
        db_table = "tag_for_cocktail"
        verbose_name = "Тег для коктейлей"
        verbose_name_plural = "Теги для коктелей"


class Cocktail(BaseModel):
    author = models.ForeignKey(BarbookUser, null=True, on_delete=models.SET_NULL)
    recipe_text = models.JSONField()
    cocktail_tag = models.ManyToManyField(
        TagForCocktail, db_table="cocktail_tag", blank=True
    )

    cocktail_like = models.ManyToManyField(
        BarbookUser, db_table="cocktail_like", related_name="likes"
    )
    barbook_user_favourite_cocktail = models.ManyToManyField(
        BarbookUser,
        db_table="barbook_user_favourite_cocktail",
        related_name="favourite",
        blank=True,
    )
    rating = models.IntegerField(default=0)

    class Meta:
        db_table = "Cocktail"
        verbose_name = "Коктейль"
        verbose_name_plural = "Коктейли"

    def __str__(self):
        return self.name


# ing -----------
class ClassForIngredientTag(models.Model):
    class_name = models.CharField(max_length=255, default="Любые")

    def __str__(self):
        return self.class_name

    class Meta:
        db_table = "class_for_ingredient_tag"
        verbose_name = "Класс для тегов ингридиента"
        verbose_name_plural = "Классы для тегов ингридиентов"


class TagForIngredient(models.Model):
    class_name = models.ForeignKey(
        ClassForIngredientTag, on_delete=models.SET_DEFAULT, default="без класса"
    )
    tag_name = models.CharField(max_length=255, default="Любые", unique=True)

    def __str__(self):
        return self.tag_name

    class Meta:
        unique_together = (("tag_name", "class_name"),)
        db_table = "tag_for_ingredient"
        verbose_name = "Тег для ингридиента"
        verbose_name_plural = "Теги для ингридиетов"


class Measures(DjangoChoices):
    milliliters = ChoiceItem(value="мл", label="мл")
    grams = ChoiceItem(value="г", label="г")


class Ingredient(BaseModel):
    ingredient_tag = models.ManyToManyField(
        TagForIngredient, db_table="ingredient_tag", related_name="tag", blank=True
    )
    measure = models.CharField(
        choices=Measures.choices, default=Measures.grams, max_length=50
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = "Ingredient"
        verbose_name = "Ингридиент"
        verbose_name_plural = "Ингридиенты"


# bar tool --------


class CocktailTool(models.Model):
    cocktail = models.ForeignKey(
        Cocktail, on_delete=models.CASCADE, related_name="cocktail_tool"
    )
    tool = models.ForeignKey("BarTool", on_delete=models.CASCADE)
    amount = models.IntegerField()

    class Meta:
        db_table = "cocktail_tool"
        verbose_name = "Инструмент"
        verbose_name_plural = "Инструменты"


class BarTool(BaseModel):
    def __str__(self):
        return self.name

    class Meta:
        db_table = "bar_tool"
        verbose_name = "Барная принадлежность"
        verbose_name_plural = "Барные принадлежности"


# recipe for cocktail --------------


class CocktailRecipe(models.Model):
    cocktail = models.ForeignKey(
        Cocktail, on_delete=models.CASCADE, related_name="recipe"
    )
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, related_name="ingredient"
    )
    amount = models.IntegerField()

    class Meta:
        db_table = "cocktail_recipe"
        verbose_name = "Рецепт коктейля(1 ингридиент)"

    def __str__(self):
        cocktail = self.cocktail.name
        ing = self.ingredient.name
        return f"{cocktail} --- {ing}"

from django.db import models
from rest_framework import serializers

from barbook_app.models import (
    Ingredient,
    BarTool,
    Cocktail,
    CocktailRecipe,
    TagForCocktail,
    ClassForCocktailTag,
    BarbookUser,
)
from barbook_app.models.stuff import CocktailTool


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ("id", "name", "small_img", "measure")


class BarToolSerializer(serializers.ModelSerializer):
    class Meta:
        model = BarTool
        fields = ("id", "name", "small_img")


class RecipeSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer(read_only=True)

    class Meta:
        model = CocktailRecipe
        fields = ("amount", "ingredient")


class CocktailUpdateSerializer(serializers.ModelSerializer):
    def to_internal_value(self, data):
        if data.get("name", None) == "":
            data.pop("name")
        if data.get("description", None) == "":
            data.pop("description")
        return super(CocktailUpdateSerializer, self).to_internal_value(data)

    class Meta:
        model = Cocktail
        read_only_fields = ("id",)
        fields = ("name", "description")


class CocktailSerializer(serializers.ModelSerializer):
    recipe = RecipeSerializer(many=True)

    class Meta:
        model = Cocktail
        fields = ("id", "img", "small_img", "description", "name", "recipe")


# -----> CreateCocktailSerializers


class CocktailToolsForCocktailCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CocktailTool
        fields = ("amount", "tool")


class RecipeForCocktailCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CocktailRecipe
        fields = ("amount", "ingredient")


class CocktailCreateSerializer(serializers.ModelSerializer):
    cocktail_tool = CocktailToolsForCocktailCreateSerializer(many=True)
    recipe = RecipeForCocktailCreateSerializer(many=True)

    def create(self, validated_data):
        print(validated_data)
        # cocktail = super(CocktailCreateSerializer, self).create(validated_data)
        cocktail = Cocktail.objects.create(
            img=validated_data["img"],
            small_img=validated_data["small_img"],
            name=validated_data["name"],
            description=validated_data["description"],
            recipe_text=validated_data["recipe_text"],
        )
        print(cocktail)
        for ing_item in validated_data["recipe"]:
            CocktailRecipe.objects.create(
                cocktail=cocktail,
                ingredient=ing_item["ingredient"],
                amount=ing_item["amount"],
            )
        for tool_item in validated_data["cocktail_tool"]:
            CocktailTool.objects.create(
                cocktail=cocktail, tool=tool_item["tool"], amount=tool_item["amount"]
            )

        cocktail = cocktail.save()

        return cocktail

    class Meta:
        model = Cocktail
        fields = (
            "img",
            "small_img",
            "cocktail_tool",
            "description",
            "name",
            "recipe",
            "recipe_text",
            "author",
        )


# ------------->
class ReturnCocktailIdAfterCreation(serializers.ModelSerializer):
    class Meta:
        model = Cocktail
        fields = ("id",)

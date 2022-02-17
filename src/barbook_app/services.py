from django.db.models import QuerySet, Count, Prefetch, Q, F
from .models import (
    ClassForCocktailTag,
    TagForCocktail,
    Ingredient,
    Cocktail,
    CocktailRecipe,
    TagForIngredient,
    BarbookUser,
    CommentOnCocktail,
)
from .models.stuff import CocktailTool, BarTool


def get_tags_and_their_classes_for_cocktail():
    classes_map = {}
    for cls in ClassForCocktailTag.objects.prefetch_related(
        "classes__cocktail_set__cocktail_tag"
    ):
        classes_map[cls.class_name] = cls.classes.all()

    return classes_map


def get_tags_and_their_classes_for_ingredient():
    tags_and_classes = TagForIngredient.objects.select_related("class_name").only(
        "tag_name", "class_name"
    )
    tags_grouped_by_class_names = {}
    for tag in tags_and_classes:
        if tags_grouped_by_class_names.get(tag.class_name.class_name):
            tags_grouped_by_class_names[tag.class_name.class_name].append(tag.tag_name)
        else:
            tags_grouped_by_class_names[tag.class_name.class_name] = [tag.tag_name]
    return tags_grouped_by_class_names


def get_cocktails_where_ingredient_is_being_used(ing: Ingredient) -> QuerySet:
    return CocktailRecipe.objects.filter(ingredient=ing).select_related("cocktail")


def get_cocktail_prepared(cocktail: Cocktail):
    cocktail_recipe = cocktail.recipe_text
    cocktail_ingredients = CocktailRecipe.objects.filter(
        cocktail=cocktail
    ).select_related(""
                     ""
                     "ingredient")
    cocktail_tools = CocktailTool.objects.filter(cocktail=cocktail).select_related(
        "tool"
    )
    cocktail_like = cocktail.cocktail_like.aggregate(Count("likes"))
    cocktail_comments = CommentOnCocktail.objects.filter(
        cocktail=cocktail
    ).select_related("author")
    return (
        cocktail_recipe,
        cocktail_ingredients,
        cocktail_tools,
        cocktail_like["likes__count"],
        cocktail_comments,
    )


def prepare_fav_cocktails_for_user_cabinet(user: BarbookUser):
    cocktails = user.favourite.all()
    dictionary = {}
    for cocktail in cocktails:
        cocktail_ingredient = CocktailRecipe.objects.filter(
            cocktail=cocktail
        ).prefetch_related("ingredient")
        for ing_ in cocktail_ingredient:
            print(ing_.ingredient.name)
        dictionary[cocktail] = cocktail_ingredient
    return dictionary


def prepare_cocktails_where_ingredient_is_being_used(ingr: Ingredient):
    recipes_list = CocktailRecipe.objects.filter(ingredient=ingr)
    cocktails_id = []
    for recipe_str in recipes_list:
        cocktails_id.append(recipe_str.cocktail_id)
    cocktails = Cocktail.objects.filter(id__in=cocktails_id)
    dictionary = {}
    for cocktail in cocktails:
        cocktail_ingredient = CocktailRecipe.objects.filter(
            cocktail=cocktail
        ).prefetch_related("ingredient")
        dictionary[cocktail] = cocktail_ingredient
    return dictionary


def new_like(cocktail_id: int, user: BarbookUser):
    cocktail = Cocktail.objects.get(id=cocktail_id)
    return_rating = cocktail.rating
    if user in cocktail.cocktail_like.all():
        cocktail.cocktail_like.remove(user)
        cocktail.rating = F("rating") - 1
        return_rating -= 1
    else:
        cocktail.cocktail_like.add(user)
        cocktail.rating = F("rating") + 1
        return_rating += 1
    cocktail.save()
    return return_rating


def get_everything_for_cocktail_creation():
    ings = Ingredient.objects.all()
    tools = BarTool.objects.all()
    tags = get_tags_and_their_classes_for_cocktail()
    return {"ingredients": ings, "tools": tools, "tags": tags}


def favorite(cocktail_id: int, user: BarbookUser):
    Cocktail.objects.get(id=cocktail_id).barbook_user_favourite_cocktail.add(user.id)


def search(search_str: str, tags: list):
    query_filter = Q()
    if tags:
        query_filter &= Q(cocktail_tag__tag_name__in=tags)
    if search_str:
        query_filter &= Q(name__iregex=search_str)
    return Cocktail.objects.filter(query_filter).distinct()


def new_comment_service(text: str, user_id: int, cocktail_id: int):
    dict = {}
    comment = CommentOnCocktail.objects.create(
        text=text, author_id=user_id, cocktail_id=cocktail_id
    )
    dict["name"] = comment.author.name
    dict["user_id"] = str(comment.author_id)
    dict["text"] = comment.text
    dict["img_url"] = comment.author.img.url
    return dict

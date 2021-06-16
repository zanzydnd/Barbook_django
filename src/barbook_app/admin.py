from django.contrib import admin
from barbook_app.models.user import BarbookUser
from barbook_app.models.stuff import (
    Ingredient,
    TagForIngredient,
    ClassForIngredientTag,
    Cocktail,
    ClassForCocktailTag,
    TagForCocktail,
    BarTool,
    CocktailRecipe,
)

from barbook_app.models.article_and_contest import Article, Contest


class TagFilter(admin.SimpleListFilter):
    title = "tag"
    parameter_name = "tag_name"

    def lookups(self, request, model_admin):
        result = ()
        for tag in TagForIngredient.objects.all():
            appender = (tag.tag_name, tag.tag_name)
            result += (appender,)
        print(result)
        return result

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(ingredient_tag__tag_name=self.value())


class IngredientModelAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "measure")
    search_fields = ("id", "name", "measure")
    list_filter = (TagFilter, "measure")


class CocktailModelAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "get_username")
    search_fields = ("id", "name")

    def get_username(self, instance: Cocktail):
        if instance.author:
            return instance.author.username
        else:
            return None

    get_username.short_description = "Username автора"
    get_username.admin_order_filed = "user__username"


admin.site.register(BarbookUser)
admin.site.register(Ingredient, IngredientModelAdmin)
admin.site.register(TagForIngredient)
admin.site.register(ClassForIngredientTag)
admin.site.register(ClassForCocktailTag)
admin.site.register(Cocktail, CocktailModelAdmin)
admin.site.register(TagForCocktail)
admin.site.register(BarTool)
admin.site.register(CocktailRecipe)
admin.site.register(Article)
admin.site.register(Contest)

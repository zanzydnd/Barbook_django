from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, re_path
from django.contrib.staticfiles.urls import static
from barbook_project import settings
from barbook_app.views import (
    Cocktails,
    main_page_view,
    Ingredients,
    IngredientDetailedView,
    CocktailDetailedView,
    registration_page,
    Authenticate,
    CabinetView,
    CreateCocktail,
    like_view,
    favorite_view,
    BarmanList_view,
    ContestsView,
    logout_view,
    search_view,
    cry_for_help_view,
    new_comment,
    drop_password_email,
    drop_pass,
)

urlpatterns = [
    path("", main_page_view, name="main"),
    path("ingredients/", Ingredients.as_view(), name="ingredients"),
    path(
        "ingredients/<int:pk>/",
        IngredientDetailedView.as_view(),
        name="ingredient_page",
    ),
    path("cocktails/", Cocktails.as_view(), name="cocktails"),
    path("cocktails/<int:pk>/", CocktailDetailedView.as_view(), name="cocktail_page"),
    path("registration/", registration_page, name="registration"),
    path("auth/", Authenticate.as_view(), name="auth"),
    re_path(r"cabinet/(?P<username>\w+)/", CabinetView.as_view(), name="cabinet"),
    path("createCocktail/", CreateCocktail.as_view(), name="createCocktail"),
    path("like/", like_view, name="like"),
    path("favourite/<int:pk>/", favorite_view, name="favorite"),
    path("barmen/", BarmanList_view.as_view(), name="barmen"),
    path("contests/", ContestsView.as_view(), name="contests"),
    path("logout/", logout_view, name="logout"),
    path("search/", search_view, name="search"),
    path("cry_for_help/", cry_for_help_view, name="help"),
    path("comments/", new_comment, name="new_comment"),
    path("drop/<str:token>/", drop_pass, name="drop"),
    path("drop_password_email/", drop_password_email, name="drop_password_email"),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

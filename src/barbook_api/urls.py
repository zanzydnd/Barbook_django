from django.urls import path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import SimpleRouter

from barbook_api.views import (
    main_api_view,
    IngredientViewSet,
    BarToolViewSet,
    cocktail_create,
    CocktailDetailsView,
    CocktailViewSet,
)

router = SimpleRouter()
router.register("ingredients", IngredientViewSet)
router.register("bartools", BarToolViewSet)
router.register("cocktails", CocktailViewSet, "cocktail_")

schema_view = get_schema_view(
    openapi.Info(
        title="Barbook API",
        default_version="v1",
        description="It's my barbook , one and only",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="ne_pishite@mne.suda"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)

urlpatterns = [
    path("", main_api_view, name="empty_api"),
    path("cocktails/", cocktail_create, name="cocktail_create"),
    *router.urls,
    re_path(
        "swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]

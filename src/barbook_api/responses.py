from drf_yasg import openapi

from barbook_api.serializers import ReturnCocktailIdAfterCreation

create_cocktail_ok_response = openapi.Response(
    "returns id of created cocktail", ReturnCocktailIdAfterCreation
)

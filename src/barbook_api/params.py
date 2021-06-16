from drf_yasg import openapi

create_cocktail_params = openapi.Parameter(
    "create", openapi.IN_QUERY, type=openapi.TYPE_OBJECT
)

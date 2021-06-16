import json

from django.contrib.auth.decorators import login_required
from django.http import Http404
from drf_yasg.utils import swagger_auto_schema
from psycopg2._json import Json
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from barbook_api.responses import create_cocktail_ok_response
from barbook_api.serializers import (
    IngredientSerializer,
    BarToolSerializer,
    CocktailSerializer,
    CocktailUpdateSerializer,
    CocktailCreateSerializer,
)
from barbook_app.models import Ingredient, BarTool, Cocktail


@api_view(["GET"])
def main_api_view(request):
    """Проверка работы api"""
    return Response({"status": "ok"})


class IngredientViewSet(viewsets.ModelViewSet):
    """Ингридиенты"""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [IsAuthenticated]


class BarToolViewSet(viewsets.ModelViewSet):
    """Барные принадлежности"""

    queryset = BarTool.objects.all()
    serializer_class = BarToolSerializer
    permission_classes = [IsAuthenticated]


@swagger_auto_schema(
    method="POST",
    responses={200: create_cocktail_ok_response},
    operation_description="Создает коктейль",
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
@login_required
@parser_classes([MultiPartParser, FormParser])
def cocktail_create(request):
    """Создание коктейля"""
    serializer = CocktailCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.create(serializer.validated_data)
        return Response(status=status.HTTP_201_CREATED)
    else:
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            content_type="multipart/form-data",
            data=json.dumps(serializer.errors),
        )


class CocktailViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "update":
            return CocktailUpdateSerializer
        return CocktailSerializer

    def get_queryset(self):
        cocktail = Cocktail.objects.all()
        return cocktail

    def list(self, request, *args, **kwargs):
        return super(CocktailViewSet, self).list(request, *args, **kwargs)


class CocktailDetailsView(APIView):
    def get_object(self, id):
        try:
            return Cocktail.objects.get(id=id)
        except Cocktail.DoesNotExist as e:
            raise Http404

    def check_object_permissions(self, request, obj):
        if request.user.is_authenticated:
            return False
        return obj.author_id == request.user.id

    def get(self, request, id):
        serializer = CocktailSerializer(self.get_object(id))
        return Response(serializer.data)

    def put(self, request, id):
        serializer = CocktailUpdateSerializer(self.get_object(id), data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        cocktail = self.get_object(id)
        cocktail.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

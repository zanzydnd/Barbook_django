from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView
from django.views import View
from django.views.generic import ListView
from rest_framework import status
from rest_framework.utils import json
import jwt

from barbook_app.models import Contest, Message, PasswordDrop
from barbook_app.forms import (
    RegistrationForm,
    AuthForm,
    LikeForm,
    CryForHelpForm,
    CommentForm,
    EmailForDroppingPassword,
    NewPassword,
)
from barbook_app.models import Cocktail, Ingredient, BarbookUser
from barbook_app.services import (
    get_tags_and_their_classes_for_cocktail,
    get_tags_and_their_classes_for_ingredient,
    get_cocktail_prepared,
    new_like,
    get_everything_for_cocktail_creation,
    favorite,
    search,
    prepare_fav_cocktails_for_user_cabinet,
    prepare_cocktails_where_ingredient_is_being_used,
    new_comment_service,
)

from barbook_app.tasks import password_update


class Cocktails(ListView):
    model = Cocktail
    template_name = "coсktails.html"
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tags"] = get_tags_and_their_classes_for_cocktail()
        return context


class CocktailDetailedView(DetailView):
    model = Cocktail
    template_name = "cocktail_info.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = get_cocktail_prepared(self.object)
        context["recipe_text"] = data[0]
        context["ingredients_list"] = data[1]
        context["tools"] = data[2]
        context["likes"] = data[3]
        context["comments"] = data[4]
        return context


class Ingredients(ListView):
    model = Ingredient
    template_name = "ingredients.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tags"] = get_tags_and_their_classes_for_ingredient()
        return context


class IngredientDetailedView(DetailView):
    model = Ingredient
    template_name = "ingredient-single.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cocktails"] = prepare_cocktails_where_ingredient_is_being_used(
            self.object
        )
        return context


def main_page_view(request):
    if not request.user.is_authenticated:
        request.user = None
    return render(request, "index.html")


def registration_page(request):
    form = RegistrationForm()
    if request.method == "GET":
        return render(request, "registration.html", {"form": form})
    elif request.method == "POST":
        form = RegistrationForm(request.POST, request.FILES)
        if form:
            if form.is_valid():
                username = form.cleaned_data["username"]
                name = form.cleaned_data["name"]
                email = form.cleaned_data["email"]
                password = form.cleaned_data["password"]
                img = form.cleaned_data["img"]
                second_name = form.cleaned_data["second_name"]
                print(img)
                role = form.cleaned_data["role"]
                password = make_password(password)
                try:
                    user = BarbookUser.objects.create(
                        username=username,
                        name=name,
                        password=password,
                        role=role,
                        email=email,
                    )
                except IntegrityError as e:
                    form.add_error(None, "Такой пользователь уже существует")
                    return render(request, "registration.html", {"form": form})
                if second_name != "":
                    user.second_name = second_name
                if img is not None:
                    user.handle_uploaded_file(request.FILES["img"])
                user.save()
                return redirect("auth")
            else:
                return render(request, "registration.html", {"form": form})
    else:
        return redirect("registration")


class Authenticate(View):
    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        form = AuthForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            lg = authenticate(username=username, password=password)

            if lg is None:
                errors = {"error": "wrong login or pass"}
                return render(request, "login.html", errors)
            else:
                login(request, lg)
                return redirect("main")
        else:
            return redirect("auth")


@login_required
def logout_view(request):
    logout(request)
    return redirect("main")


class CabinetView(DetailView):
    model = BarbookUser
    template_name = "personalcabinet.html"
    username_from_url = "username"

    def get_object(self, **kwargs):
        print(self.kwargs["username"])
        return get_object_or_404(BarbookUser, username=self.kwargs["username"])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["favourites"] = prepare_fav_cocktails_for_user_cabinet(self.object)
        return context


class CreateCocktail(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, "own_creation.html")


@login_required()
def like_view(request):
    if request.method == "POST":
        form = LikeForm(request.POST)
        if form.is_valid():
            likes = new_like(form.cleaned_data["cockt_id"], request.user)
        else:
            return HttpResponse("")
        return HttpResponse(
            json.dumps({"num_of_likes": likes}), content_type="application/json"
        )
    else:
        return HttpResponse(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@login_required
def favorite_view(request, pk):
    if request.method == "POST":
        favourite = favorite(pk, request.user)
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class BarmanList_view(ListView):
    model = BarbookUser
    template_name = "barmen-list.html"


class ContestsView(ListView):
    model = Contest
    template_name = "contests.html"


def search_view(request):
    if request.method == "POST":
        result = search(
            request.POST.get("search"), json.loads(request.POST.get("tags"))
        )
        if result:
            data = serializers.serialize(
                "json", list(result), fields=("id", "small_img", "name")
            )
            return HttpResponse(data, content_type="application/json")
        else:
            return HttpResponse(None)


def cry_for_help_view(request):
    if request.method == "POST":
        form = CryForHelpForm(request.POST)
        if form.is_valid():
            Message.objects.create(
                author_email=form.cleaned_data["author_email"],
                author_name=form.cleaned_data["author_name"],
                message_text=form.cleaned_data["message_text"],
            )
        return render(request, "index.html")
    else:
        return HttpResponse(status=status.HTTP_405_METHOD_NOT_ALLOWED)


def drop_password_email(request):
    if request.method == "POST":
        email_form = EmailForDroppingPassword(request.POST)
        if email_form.is_valid():
            email = email_form.cleaned_data["email"]
            jwt_token = jwt.encode({"mail": email}, "secret", algorithm="HS256")
            uri = request.build_absolute_uri(reverse("drop", args=(jwt_token,)))
            password_update.delay(jwt_token, uri)
            return redirect("main")
        else:
            return redirect("main")
    else:
        return render(request, "drop_password_email.html")


def drop_pass(request, token):
    pass_drop = PasswordDrop.objects.get(jwt_token=token)
    if not pass_drop:
        return redirect(request, "main")
    if request.method == "GET":
        return render(request, "new_password.html")
    elif request.method == "POST":
        password_form = NewPassword(request.POST)
        if password_form.is_valid():
            new_pass = make_password(password_form.cleaned_data["password"])
            pass_drop.user.password = new_pass
            pass_drop.user.save()
            pass_drop.delete()
            return redirect("auth")
        else:
            return redirect(request, "main")


def new_comment(request):
    if request.method == "POST":
        form = CommentForm(request.POST)
        print("1")
        if form.is_valid():
            return HttpResponse(
                json.dumps(
                    new_comment_service(
                        form.cleaned_data["text"],
                        form.cleaned_data["user_id"],
                        form.cleaned_data["cocktail_id"],
                    )
                ),
                content_type="application/json",
            )
        else:
            return HttpResponse(status=400)
    else:
        return HttpResponse(status=405)

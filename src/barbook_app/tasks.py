from django.core.mail import send_mail
from django.http import HttpRequest
from rest_framework.reverse import reverse
from barbook_app.models import PasswordDrop, BarbookUser, Cocktail
from barbook_app.parse import get_cocktails
from barbook_project import settings
from barbook_project.celery import app
import jwt


# @app.task
# def cocktails_validate():
#     cockts = []
#     profanity.load_censor_words()
#     for cocktail in Cocktail.objects.all():
#         cocktail.name = profanity.censor(cocktail.name)
#         cocktail.description = profanity.censor(cocktail.description)
#         cockts.append(cocktail)
#     Cocktail.objects.bulk_update(cockts, ["name", "description"])


@app.task
def password_update(jwt_token, uri):
    print("password_update")
    email = jwt.decode(jwt_token, "secret", algorithms=["HS256"])["mail"]
    obj, created = PasswordDrop.objects.get_or_create(
        user=BarbookUser.objects.get(email=email), jwt_token=jwt_token
    )
    if not created:
        obj.delete()
        obj = PasswordDrop.objects.create(
            user=BarbookUser.objects.get(email=email), jwt_token=jwt_token
        )
    email_text = f"Your link for dropping password {uri}"
    send_mail(
        "Password dropping",
        email_text,
        settings.DEFAULT_FROM_EMAIL,
        [email],
    )

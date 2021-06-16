from django.db import models

from barbook_app.models import BarbookUser


class PasswordDrop(models.Model):
    user = models.ForeignKey(BarbookUser, on_delete=models.DO_NOTHING)
    jwt_token = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = "drop_password"

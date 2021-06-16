import os
import uuid
from datetime import datetime

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import (
    PermissionsMixin,
    UserManager as DjangoUserManager,
)
from django.core.files import File
from django.db import models
from djchoices import DjangoChoices, ChoiceItem


class UserManager(DjangoUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        user = self.model(email=email, username=username)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        user = self.model(email=email, username=username, is_superuser=True)
        user.set_password(password)
        user.save()
        return user


class Role(DjangoChoices):
    amateur = ChoiceItem(value="любитель", label="любитель")
    bartender = ChoiceItem(value="профессионал", label="профессионал")


class BarbookUser(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()

    email = models.EmailField(unique=True, null=False, default="email@email.com")
    role = models.CharField(choices=Role.choices, default=Role.amateur, max_length=50)
    img = models.ImageField(
        upload_to="img_source/img", default="img_source/img/default.jpg", null=False
    )
    name = models.CharField(max_length=255, null=False, default="Бармен")
    second_name = models.CharField(max_length=255, default="Барменович", null=False)
    username = models.CharField(max_length=30, unique=True)

    @property
    def is_staff(self):
        return self.is_superuser

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "password"]

    def handle_uploaded_file(self, file: File):
        da = datetime.now()
        self.img.save(
            os.path.basename(
                str(da.time()) + str(da.date()) + uuid.uuid4().hex + file.name
            ),
            file,
        )
        self.save()

    class Meta:
        db_table = "BarbookUser"
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class JobRole(DjangoChoices):
    pr = ChoiceItem(label="PR", value="PR")
    admin = ChoiceItem(label="Администратор", value="Администратор")
    ambassador = ChoiceItem(label="Амбассадор бренда", value="Амбассадор бренда")
    barman = ChoiceItem(label="Бармен", value="Бармен")
    brand_manager = ChoiceItem(label="Бренд менеджер", value="Бренд менеджер")
    owner = ChoiceItem(label="Владелец", value="Владелец")
    director = ChoiceItem(label="Директор", value="Директор")
    bar_manager = ChoiceItem(label="Менеджер", value="Менеджер")
    waiter = ChoiceItem(label="Официант", value="Официант")
    barman_helper = ChoiceItem(label="Помощник бармена", value="Помощник бармена")
    senior_barman = ChoiceItem(label="Старший бармен", value="Старший бармен")
    hostess = ChoiceItem(label="Хостесс", value="Хостесс")
    chef = ChoiceItem(label="Шеф-повар", value="Шеф-повар")


class BarbookUserJobHistory(models.Model):
    place_name = models.CharField(max_length=255)
    date_beginning = models.DateField()
    date_ending = models.DateField(null=True)
    user = models.ForeignKey(BarbookUser, on_delete=models.CASCADE)
    still = models.BooleanField()
    job_role = models.CharField(choices=JobRole, default=JobRole.barman, max_length=255)
    country = models.CharField(max_length=255, default="Страна")
    city = models.CharField(max_length=255, default="Город")

    class Meta:
        db_table = "barbook_user_job_history"
        verbose_name_plural = "Места работы"
        verbose_name = "Место работы"

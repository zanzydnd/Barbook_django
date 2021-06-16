from django.db import models


class Article(models.Model):
    text = models.TextField(max_length=1000)
    header = models.CharField(max_length=255)
    img = models.ImageField()
    date = models.DateField(auto_now=True)

    class Meta:
        db_table = "article"
        verbose_name = "Новость"
        verbose_name_plural = "Новости"

    def __str__(self):
        return self.header


class Contest(models.Model):
    img = models.ImageField()
    date = models.DateField()
    info = models.TextField(max_length=255)
    name = models.CharField(max_length=40)
    url = models.URLField()

    class Meta:
        db_table = "contest"
        verbose_name = "Конкурс"
        verbose_name_plural = "Конкурсы"

    def __str__(self):
        return self.name

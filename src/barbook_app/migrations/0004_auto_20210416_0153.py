# Generated by Django 3.1.7 on 2021-04-15 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("barbook_app", "0003_auto_20210415_2028"),
    ]

    operations = [
        migrations.AddField(
            model_name="cocktail",
            name="rating",
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name="barbookuser",
            name="img",
            field=models.ImageField(
                default="img_source/img/default.jpg", upload_to="img_source/img"
            ),
        ),
    ]

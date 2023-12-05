# Generated by Django 4.2.7 on 2023-11-27 07:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="image",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="product/%Y/%m/%d/",
                verbose_name="Фото",
            ),
        ),
    ]

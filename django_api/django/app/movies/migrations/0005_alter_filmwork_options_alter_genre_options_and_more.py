# Generated by Django 4.2.5 on 2023-10-12 16:40

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("movies", "0004_alter_personfilmwork_role"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="filmwork",
            options={"verbose_name": "Filmwork", "verbose_name_plural": "Filmworks"},
        ),
        migrations.AlterModelOptions(
            name="genre",
            options={"verbose_name": "Genre", "verbose_name_plural": "Genres"},
        ),
        migrations.AlterModelOptions(
            name="genrefilmwork",
            options={
                "verbose_name": "Filmwork genre",
                "verbose_name_plural": "Filmwork genres",
            },
        ),
        migrations.AlterModelOptions(
            name="person",
            options={"verbose_name": "Person", "verbose_name_plural": "Persons"},
        ),
        migrations.AlterModelOptions(
            name="personfilmwork",
            options={
                "verbose_name": "Filmwork person",
                "verbose_name_plural": "Filmwork persons",
            },
        ),
    ]
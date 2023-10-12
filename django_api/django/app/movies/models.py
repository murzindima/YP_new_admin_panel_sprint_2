import uuid

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    created_at = models.DateTimeField(_("created"), auto_now_add=True)
    updated_at = models.DateTimeField(_("modified"), auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, verbose_name=_("id")
    )

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_("name"), max_length=255)
    description = models.TextField(_("description"), null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'content"."genre'
        verbose_name = _("Genre")
        verbose_name_plural = _("Genres")


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField(_("full_name"), max_length=255, db_index=True)

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = 'content"."person'
        verbose_name = _("Person")
        verbose_name_plural = _("Persons")


class FilmworkType(models.TextChoices):
    MOVIE = "movie", _("movie")
    TV_SHOW = "tv_show", _("tv_show")


class Filmwork(UUIDMixin, TimeStampedMixin):
    title = models.CharField(_("title"), max_length=255, db_index=True)
    description = models.TextField(_("description"), null=True)
    creation_date = models.DateField(_("creation_date"), null=True, db_index=True)
    rating = models.FloatField(
        _("rating"),
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        db_index=True,
    )
    type = models.CharField(
        _("type"),
        choices=FilmworkType.choices,
        default=FilmworkType.MOVIE,
        max_length=7,
    )
    genres = models.ManyToManyField(
        Genre, through="GenreFilmwork", verbose_name=_("genres")
    )
    persons = models.ManyToManyField(
        Person, through="PersonFilmwork", verbose_name=_("persons")
    )

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'content"."film_work'
        verbose_name = _("Filmwork")
        verbose_name_plural = _("Filmworks")


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey(
        "Filmwork", on_delete=models.CASCADE, verbose_name=_("film_work")
    )
    genre = models.ForeignKey(
        "Genre", on_delete=models.CASCADE, verbose_name=_("genre")
    )
    created_at = models.DateTimeField(_("created"), auto_now_add=True)

    class Meta:
        db_table = 'content"."genre_film_work'
        verbose_name = _("Filmwork Genre")
        verbose_name_plural = _("Filmwork Genres")
        constraints = [
            models.UniqueConstraint(
                fields=["film_work_id", "genre_id"], name="film_work_genre"
            )
        ]


class PersonFilmworkRole(models.TextChoices):
    ACTOR = "actor", _("actor")
    WRITER = "writer", _("writer")
    DIRECTOR = "director", _("director")


class PersonFilmwork(UUIDMixin):
    film_work = models.ForeignKey(
        "Filmwork", on_delete=models.CASCADE, verbose_name=_("film_work")
    )
    person = models.ForeignKey(
        "Person", on_delete=models.CASCADE, verbose_name=_("person")
    )
    role = models.CharField(
        _("role"),
        choices=PersonFilmworkRole.choices,
        default=PersonFilmworkRole.ACTOR,
        max_length=8,
    )
    created_at = models.DateTimeField(_("created"), auto_now_add=True)

    class Meta:
        db_table = 'content"."person_film_work'
        verbose_name = _("Filmwork Person")
        verbose_name_plural = _("Filmwork Persons")
        constraints = [
            models.UniqueConstraint(
                fields=["film_work_id", "person_id", "role"],
                name="film_work_person_role",
            )
        ]

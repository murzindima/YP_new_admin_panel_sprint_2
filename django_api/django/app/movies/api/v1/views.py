from django.db.models import Prefetch
from django.http import JsonResponse
# from django.core import serializers
from django.views.generic.list import BaseListView

from movies.models import Filmwork, Genre, PersonFilmwork, PersonFilmworkRole


class MoviesListApi(BaseListView):
    model = Filmwork
    http_method_names = ['get']

    def get_queryset(self):
        movies = (
            Filmwork.objects.all()
            .prefetch_related(
                Prefetch('genres', queryset=Genre.objects.all()),
                Prefetch('personfilmwork_set', queryset=PersonFilmwork.objects.filter(role=PersonFilmworkRole.ACTOR),
                         to_attr='actors'),
                Prefetch('personfilmwork_set', queryset=PersonFilmwork.objects.filter(role=PersonFilmworkRole.DIRECTOR),
                         to_attr='directors'),
                Prefetch('personfilmwork_set', queryset=PersonFilmwork.objects.filter(role=PersonFilmworkRole.WRITER),
                         to_attr='writers'),
            )
        )
        return movies

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = self.get_queryset()
        serialized_results = []

        for film_work in queryset:
            serialized_results.append({
                'id': str(film_work.id),
                'title': film_work.title,
                'description': film_work.description,
                'creation_date': film_work.creation_date,
                'rating': film_work.rating,
                'type': film_work.type,
                'genres': [genre.name for genre in film_work.genres.all()],
                'actors': [person_film_work.person.full_name for person_film_work in film_work.actors],
                'directors': [person_film_work.person.full_name for person_film_work in film_work.directors],
                'writers': [person_film_work.person.full_name for person_film_work in film_work.writers],
            })

        context = {
            'results': serialized_results,
        }
        return context

    @staticmethod
    def render_to_response(context):
        return JsonResponse(context)

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return self.render_to_response(context)

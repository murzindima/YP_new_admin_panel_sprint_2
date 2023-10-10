from django.contrib.postgres.aggregates import ArrayAgg
from django.http import JsonResponse
from django.views.generic.list import BaseListView
from django.db.models import Q

from movies.models import Filmwork, Genre, PersonFilmwork, PersonFilmworkRole


class MoviesListApi(BaseListView):
    model = Filmwork
    http_method_names = ['get']

    def get_queryset(self):
        movies = (
            Filmwork.objects.all()
            .annotate(
                genre_names=ArrayAgg('genres__name'),
                actor_names=ArrayAgg('personfilmwork__person__full_name',
                                     filter=Q(personfilmwork__role=PersonFilmworkRole.ACTOR)),
                director_names=ArrayAgg('personfilmwork__person__full_name',
                                        filter=Q(personfilmwork__role=PersonFilmworkRole.DIRECTOR)),
                writer_names=ArrayAgg('personfilmwork__person__full_name',
                                      filter=Q(personfilmwork__role=PersonFilmworkRole.WRITER))
            )
            .values('id', 'title', 'description', 'creation_date', 'rating', 'type', 'genre_names', 'actor_names',
                    'director_names', 'writer_names')
        )
        return movies

    def get_context_data(self, *, object_list=None, **kwargs):
        context = {
            'results': list(self.get_queryset())
        }
        return context

    @staticmethod
    def render_to_response(context):
        return JsonResponse(context)

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return self.render_to_response(context)

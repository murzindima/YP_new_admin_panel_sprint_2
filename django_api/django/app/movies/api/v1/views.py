from django.contrib.postgres.aggregates import ArrayAgg
from django.http import JsonResponse, Http404
from django.views.generic.list import BaseListView
from django.views.generic.detail import BaseDetailView
from django.db.models import Q

from movies.models import Filmwork, Genre, PersonFilmwork, PersonFilmworkRole


class MoviesApiMixin:
    model = Filmwork
    http_method_names = ['get']

    def get_queryset(self):
        movies = (
            Filmwork.objects.all().order_by('id')
            .annotate(
                genre_names=ArrayAgg('genres__name', distinct=True),
                actor_names=ArrayAgg('personfilmwork__person__full_name',
                                     filter=Q(personfilmwork__role=PersonFilmworkRole.ACTOR), distinct=True),
                director_names=ArrayAgg('personfilmwork__person__full_name',
                                        filter=Q(personfilmwork__role=PersonFilmworkRole.DIRECTOR), distinct=True),
                writer_names=ArrayAgg('personfilmwork__person__full_name',
                                      filter=Q(personfilmwork__role=PersonFilmworkRole.WRITER), distinct=True)
            )
            .values('id', 'title', 'description', 'creation_date', 'rating', 'type', 'genre_names', 'actor_names',
                    'director_names', 'writer_names')
        )
        return movies

    @staticmethod
    def render_to_response(context):
        return JsonResponse(context)


class MoviesListApi(MoviesApiMixin, BaseListView):
    paginate_by = 50

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = self.get_queryset()
        paginator, page, queryset, is_paginated = self.paginate_queryset(queryset, self.paginate_by)
        context = {
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'prev': page.previous_page_number() if page.has_previous() else None,
            'next': page.next_page_number() if page.has_next() else None,
            'results': list(queryset),
        }
        return context


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):

    def get_object(self, queryset=None):
        """Override get_object to fetch a dictionary representation of the movie."""
        queryset = self.get_queryset()
        # Filter by primary key from the URL
        obj = queryset.filter(id=self.kwargs['pk']).first()

        if not obj:
            raise Http404("No movie found matching the query")

        return obj

    def get_context_data(self, **kwargs):
        obj = self.get_object()
        context = {
            'id': obj['id'],
            'title': obj['title'],
            'description': obj['description'],
            'creation_date': obj['creation_date'],
            'rating': obj['rating'],
            'type': obj['type'],
            'genre_names': obj['genre_names'],
            'actor_names': obj['actor_names'],
            'director_names': obj['director_names'],
            'writer_names': obj['writer_names'],
        }
        return context


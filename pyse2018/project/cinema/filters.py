import django_filters
from django_filters.rest_framework import FilterSet

from cinema.models import (
    Filme,
    Sessao,
    Ingresso,
)


class FilmeFilter(FilterSet):
    da_cidade = django_filters.CharFilter(label='Da Cidade', method='filter_da_cidade')
    do_cinema = django_filters.CharFilter(label='Do Cinema', method='filter_do_cinema')
    de_hoje = django_filters.BooleanFilter(label='De Hoje', method='filter_de_hoje')

    class Meta:
        model = Filme
        fields = ['titulo', 'genero', 'da_cidade', 'do_cinema', 'de_hoje']

    def filter_da_cidade(self, queryset, name, value):
        return queryset.da_cidade(value)

    def filter_do_cinema(self, queryset, name, value):
        return queryset.do_cinema(value)

    def filter_de_hoje(self, queryset, name, value):
        if value:
            return queryset.de_hoje()
        return queryset



class SessaoFilter(FilterSet):
    do_filme = django_filters.CharFilter(label='Do Filme', method='filter_do_filme')
    da_cidade = django_filters.CharFilter(label='Da Cidade', method='filter_da_cidade')
    do_cinema = django_filters.CharFilter(label='Do Cinema', method='filter_do_cinema')
    de_hoje = django_filters.BooleanFilter(label='De Hoje', method='filter_de_hoje')
    lotadas = django_filters.BooleanFilter(label='Lotadas', method='filter_lotadas')
    livres = django_filters.BooleanFilter(label='Livres', method='filter_livres')

    class Meta:
        model = Sessao
        fields = ['sala', 'filme', 'inicio', 'fim', 'preco', 'da_cidade', 'do_cinema', 'de_hoje']

    def filter_do_filme(self, queryset, name, value):
        return queryset.do_filme(value)

    def filter_da_cidade(self, queryset, name, value):
        return queryset.da_cidade(value)

    def filter_do_cinema(self, queryset, name, value):
        return queryset.do_cinema(value)

    def filter_de_hoje(self, queryset, name, value):
        if value:
            return queryset.de_hoje()
        return queryset

    def filter_lotadas(self, queryset, name, value):
        if value:
            return queryset.lotadas()
        return queryset

    def filter_livres(self, queryset, name, value):
        if value:
            return queryset.livres()
        return queryset


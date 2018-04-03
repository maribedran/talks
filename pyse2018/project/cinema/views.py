from django_filters import rest_framework as filters
from rest_framework.viewsets import ModelViewSet

from cinema.models import (
    Filme,
    Cidade,
    Cinema,
    Sala,
    Sessao,
    Ingresso,
)
from cinema.filters import FilmeFilter, SessaoFilter
from cinema.serializers import (
    FilmeSerializer,
    CidadeSerializer,
    CinemaSerializer,
    SalaSerializer,
    SessaoSerializer,
    IngressoSerializer,
)


class FilmeViewSet(ModelViewSet):
    queryset = Filme.objects.all()
    serializer_class = FilmeSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = FilmeFilter


class CidadeViewSet(ModelViewSet):
    queryset = Cidade.objects.all()
    serializer_class = CidadeSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('nome', )


class CinemaViewSet(ModelViewSet):
    queryset = Cinema.objects.all()
    serializer_class = CinemaSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('nome', 'cidade', )


class SalaViewSet(ModelViewSet):
    queryset = Sala.objects.all()
    serializer_class = SalaSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('nome', 'lotacao', 'cinema', )


class SessaoViewSet(ModelViewSet):
    queryset = Sessao.objects.all()
    serializer_class = SessaoSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = SessaoFilter


class IngressoViewSet(ModelViewSet):
    queryset = Ingresso.objects.all()
    serializer_class = IngressoSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('sessao', 'meia_entrada', )


from rest_framework.viewsets import ModelViewSet

from cinema.models import (
    Filme,
    Cidade,
    Cinema,
    Sala,
    Sessao,
    Ingresso,
)
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


class CidadeViewSet(ModelViewSet):
    queryset = Cidade.objects.all()
    serializer_class = CidadeSerializer


class CinemaViewSet(ModelViewSet):
    queryset = Cinema.objects.all()
    serializer_class = CinemaSerializer


class SalaViewSet(ModelViewSet):
    queryset = Sala.objects.all()
    serializer_class = SalaSerializer


class SessaoViewSet(ModelViewSet):
    queryset = Sessao.objects.all()
    serializer_class = SessaoSerializer


class IngressoViewSet(ModelViewSet):
    queryset = Ingresso.objects.all()
    serializer_class = IngressoSerializer


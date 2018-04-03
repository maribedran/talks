from django.urls import include, path
from rest_framework.routers import SimpleRouter

from cinema.views import (
    FilmeViewSet,
    CidadeViewSet,
    CinemaViewSet,
    SalaViewSet,
    SessaoViewSet,
    IngressoViewSet,
)


router = SimpleRouter()

router.register(r'filmes', FilmeViewSet, base_name='filmes')
router.register(r'cidades', CidadeViewSet, base_name='cidades')
router.register(r'cinemas', CinemaViewSet, base_name='cinemas')
router.register(r'salas', SalaViewSet, base_name='salas')
router.register(r'sessoes', SessaoViewSet, base_name='sessoes')
router.register(r'ingressos', IngressoViewSet, base_name='ingressos')

app_name = 'cinema'

urlpatterns = [
    path('', include(router.urls))
]


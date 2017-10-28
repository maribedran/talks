from django.conf.urls import include, url

from cinema.views import (
    FilmeCreateView,
    FilmeDeleteView,
    FilmeDetailView,
    FilmeUpdateView,
    FilmeListView,
    SessaoListView,
)

urlpatterns = [
    url(r'^$', FilmeListView.as_view(), name='filme-list'),
    url(r'^criar/$', FilmeCreateView.as_view(), name='filme-create'),
    url(r'^(?P<pk>[0-9]+)/$', FilmeDetailView.as_view(), name='filme-detail'),
    url(r'^(?P<pk>[0-9]+)/editar/$', FilmeUpdateView.as_view(), name='filme-update'),
    url(r'^(?P<pk>[0-9]+)/remover/$', FilmeDeleteView.as_view(), name='filme-delete'),
    url(r'^sessoes/$', SessaoListView.as_view(), name='sessao-list'),
]

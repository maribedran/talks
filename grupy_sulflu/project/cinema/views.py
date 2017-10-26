from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.urls import reverse_lazy

from cinema.models import Filme


class FilmeListView(ListView):
    model = Filme


class FilmeDetailView(DetailView):
    model = Filme


class FilmeCreateView(CreateView):
    model = Filme
    fields = ['titulo']
    success_url = reverse_lazy('filme-list')


class FilmeUpdateView(UpdateView):
    model = Filme
    fields = ['titulo']
    success_url = reverse_lazy('filme-list')


class FilmeDeleteView(DeleteView):
    model = Filme
    success_url = reverse_lazy('filme-list')

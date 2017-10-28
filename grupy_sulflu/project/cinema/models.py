from datetime import date
from django.db import models
from django.db.models import Count, F

# QuerySets

class FilmeQuerySet(models.QuerySet):
    def da_cidade(self, nome_cidade):
        return self.filter(
            sessoes__sala__cinema__cidade__nome__contains=nome_cidade
        )

    def do_cinema(self, nome_cinema):
        return self.filter(
            sessoes__sala__cinema__nome__contains=nome_cinema
        )

    def de_hoje(self):
        return self.filter(sessoes__inicio__date=date.today())


class SessaoQuerySet(models.QuerySet):
    def do_filme(self, nome_filme):
        return self.filter(filme__titulo__contains=nome_filme)

    def da_cidade(self, nome_cidade):
        return self.filter(sala__cinema__cidade__nome__contains=nome_cidade)

    def do_cinema(self, nome_cinema):
        return self.filter(sala__cinema__nome__contains=nome_cinema)

    def de_hoje(self):
        return self.filter(inicio__date=date.today())

    def lotadas(self):
        return self.annotate(
            ocupacao=Count('ingressos')
        ).filter(sala__lotacao__lte=F('ocupacao'))

    def livres(self):
        return self.annotate(
            ocupacao=Count('ingressos')
        ).filter(sala__lotacao__gte=F('ocupacao'))


# Managers

class FilmeManager(models.Manager):
    def get_queryset(self):
        return FilmeQuerySet(self.model, using=self._db)

    def da_cidade(self, nome_cidade):
        return self.get_queryset().da_cidade(nome_cidade)

    def do_cinema(self, nome_cinema):
        return self.get_queryset().do_cinema(nome_cinema)

    def de_hoje(self):
        return self.get_queryset().de_hoje()


class SessaoManager(models.Manager):
    def get_queryset(self):
        return SessaoQuerySet(self.model, using=self._db)

    def filme(self, nome_filme):
        return self.get_queryset().do_filme(nome_filme)

    def cidade(self, nome_cidade):
        return self.get_queryset().da_cidade(nome_cidade)

    def cinema(self, nome_cinema):
        return self.get_queryset().do_cinema(nome_cinema)

    def hoje(self):
        return self.get_queryset().de_hoje()

    def lotadas(self):
        return self.get_queryset().lotadas()

    def livres(self):
        return self.get_queryset().livres()

# Modelos

class Filme(models.Model):
    titulo = models.CharField(max_length=255)

    objects = FilmeManager()

    def __str__(self):
        return self.titulo


class Cidade(models.Model):
    nome = models.CharField(max_length=50)


class Cinema(models.Model):
    nome = models.CharField(max_length=50)
    cidade = models.ForeignKey(Cidade)


class Sala(models.Model):
    nome = models.CharField(max_length=10)
    cinema = models.ForeignKey(Cinema, related_name='salas')
    lotacao = models.IntegerField()


class Sessao(models.Model):
    sala = models.ForeignKey(Sala, related_name='sessoes')
    filme = models.ForeignKey(Filme, related_name='sessoes')
    inicio = models.DateTimeField()
    fim = models.DateTimeField()

    objects = SessaoManager()


class Ingresso(models.Model):
    sessao = models.ForeignKey(Sessao, related_name='ingressos')



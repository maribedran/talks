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

# Atenção! As opções não garantem validação a menos que seja chamado o método clean
GENEROS = (
  ('ACAO', 'Ação'),
  ('COMEDIA', 'Comédia'),
  ('DOCUMENTARIO', 'Documentário'),
  ('DRAMA', 'Drama'),
  ('INFANTIL', 'Infantil'),
  ('ROMANCE', 'Romance'),
  ('TERROR', 'Terror'),
)

class Filme(models.Model):
    titulo = models.CharField('Título', max_length=255)
    genero = models.CharField('Gênero', max_length=100, choices=GENEROS)

    objects = FilmeManager()

    def __str__(self):
        return self.titulo


class Cidade(models.Model):
    nome = models.CharField('Cidade', max_length=50)

    def __str__(self):
        return self.nome


class Cinema(models.Model):
    nome = models.CharField('Nome', max_length=50)
    cidade = models.ForeignKey(Cidade, related_name='cinemas', on_delete=models.CASCADE)

    def __str__(self):
        return self.nome


class Sala(models.Model):
    nome = models.CharField(max_length=10)
    cinema = models.ForeignKey(Cinema, related_name='salas', on_delete=models.CASCADE)
    lotacao = models.PositiveIntegerField('Lotação')

    def __str__(self):
        # Cuidado com a query a mais para acessar cinema
        return f'Sala {self.nome} - {self.cinema.nome}'


class Sessao(models.Model):
    sala = models.ForeignKey(Sala, related_name='sessoes', on_delete=models.CASCADE)
    filme = models.ForeignKey(Filme, related_name='sessoes', on_delete=models.CASCADE)
    inicio = models.DateTimeField('Início')
    fim = models.DateTimeField('Fim')

    objects = SessaoManager()

    def __str__(self):
        return f'Sessão de {self.inicio.time().strftime("%h:%M")} dia {self.inicio.date().strftime("%d/%m/%Y")}'


class Ingresso(models.Model):
    sessao = models.ForeignKey(Sessao, related_name='ingressos', on_delete=models.CASCADE)
    preco = models.DecimalField('Preço', max_digits=5, decimal_places=2)
    meia_entrada = models.BooleanField('Meia entrada', default=False)
    assento = models.CharField('Assento', max_length=4, null=True, blank=True)

    @property
    def valor(self):
        return self.preco / 2 if self.meia_entrada else self.preco

    def __str__(self):
        texto = f'R$ {self.valor}'
        texto += f' - assento {self.assento}' if self.assento else ''
        return texto


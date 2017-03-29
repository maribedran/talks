===============
Django Managers
===============


----


O Modelo
========

Um modelo no django é uma classe que representa uma entrada em uma tabela no banco de dados.

.. code:: python

  from django.db import models


  class Filme(models.Model):
      titulo = models.CharField(max_length=255)


Uma instância do modelo representa apenas uma entrada no banco, para acessar e manipular conjuntos de entradas o django tem as classes de **managers**.


----


O Manager
=========

Todo modelo no django tem implicitamante uma manager que é acessado pelo atributo de classe ``objects``, ele é responsável por fazer a interface entre o modelo e as operações no banco. Podemos customizar o manager do nosso modelo criando uma classe que herde de ``models.Manager``

.. code:: python

  from django.db import models


  class FilmeManager(models.Manager):
      pass


  class Filme(models.Model):
      titulo = models.CharField(max_length=255)

      objects = FilmeManager()


----

O QuerySet
==========

Todas as tarefas de consulta no banco realizadas pelos managers são chamadas a uma classe de ``models.QuerySet``, que pode ser customizada da mesma forma que se faz com o manager.

.. code:: python

  class FilmeQuerySet(models.QuerySet):
      pass

  class FilmeManager(models.Manager):
      def get_queryset(self):
          return FilmeQuerySet(self.model, using=self._db)

      def get(self, *args, **kwargs):
          return self.get_queryset().get(*args, **kwargs)

  class Filme(models.Model):
      titulo = models.CharField(max_length=255)

      objects = FilmeManager()


Todos os métodos de consulta no banco que usamos do ``objects`` padrão do modelo, como ``get`` e ``filter`` retornam chamadas de métodos com o mesmo nome do ``QuerySet`` do modelo.

----

Um pouco de contexto
====================

.. code:: python

  class Filme(models.Model):
      titulo = models.CharField(max_length=255)

      objects = FilmeManager()


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


----

=====================
Os métodos de manager
=====================

Métodos que retornam instâncias do modelo
=========================================

- ``get``
- ``first``
- ``last``
- ``earliest``
- ``latest``


.. code:: python

  >>> Filme.objects.get(titulo='Exterminador do Futuro')
  <Filme: Exterminador do Futuro>
  >>> Filme.objects.first()
  <Filme: Exterminador do Futuro>
  >>> Filme.objects.last()
  <Filme: Exterminador do Futuro>
  >>> Filme.objects.earliest('id')
  <Filme: Exterminador do Futuro>
  >>> Filme.objects.latest('id')
  <Filme: Exterminador do Futuro>

----

Métodos que criam, atualizam e deletam
======================================

- ``create``
- ``update``
- ``get_or_create``
- ``update_or_create``
- ``bulk_create``
- ``delete``

.. code:: python

  >>> Filme.objects.create(titulo='Exterminador do Futuro')
  Filme: Exterminador do Futuro>
  >>> Filme.objects.update(titulo='Exterminador do Futuro 2')
  1
  >>> Filme.objects.get_or_create(titulo='Curtindo a Vida Adoidado')
  (<Filme: Curtindo a Vida Adoidado>, True)
  >>> Filme.objects.update_or_create(pk=1, defaults={'titulo': 'Batman'})
  (<Filme: Batman>, False)
  >>> Filme.objects.bulk_create([Filme(titulo='Rambo'), Filme(titulo='Rambo 2')])
  [<Filme: Rambo>, <Filme: Rambo 2>]
  >>> Filme.objects.all().delete()
  (4, {u'cinema.Filme': 4})


----


Métodos que realizam consultas no banco
=======================================

1) Métodos que retornam querysets

- ``all``
- ``none``
- ``filter``
- ``exclude``
- ``order_by``
- ``reverse``
- ``distinct``
- ``values``
- ``values_list``
- ``select_related``
- ``prefetch_related``

  Todos os métodos que retornam querysets podem ter chamadas encadeadas e a execução deles é *lazzy*, ou seja, é possível chamar vários métodos que fazem queries diferentes, mas que só serão executadas uma vez.

----

Métodos que realizam consultas no banco
=======================================

.. code:: python

  >>> Filme.objects.all()
  <QuerySet [<Filme: Rambo>, <Filme: Rambo 2>]>

  >>> Filme.objects.none()
  <QuerySet []>

  >>> Filme.objects.filter(titulo='Batman')
  <QuerySet [<Filme: Batman>]>

  >>> Filme.objects.exclude(titulo__contains='Rambo')
  <QuerySet [<Filme: Batman>, <Filme: Curtindo a Vida Adoidado>]>

  >>> Filme.objects.order_by('titulo')
  <QuerySet [<Filme: Batman>, <Filme: Curtindo a Vida Adoidado>, <Filme: Rambo>, <Filme: Rambo 2>]>

  >>> Filme.objects.annotate(salas=F('sessoes__sala__nome'))
  <QuerySet [<Filme: Batman>, <Filme: Rambo>, <Filme: Rambo 2>, <Filme: Curtindo a Vida Adoidado>]>
  >>> Filme.objects.annotate(salas=F('sessoes__sala__nome')).first().salas
  u'1'

  >>> Filme.objects.reverse()
  <QuerySet [<Filme: Batman>, <Filme: Rambo>, <Filme: Rambo 2>, <Filme: Curtindo a Vida Adoidado>]>

  >>> Filme.objects.distinct()
  <QuerySet [<Filme: Batman>, <Filme: Rambo>, <Filme: Rambo 2>, <Filme: Curtindo a Vida Adoidado>]>


----

Métodos que realizam consultas no banco
=======================================

.. code:: python

  >>> Filme.objects.values()
  <QuerySet [{'titulo': u'Batman', u'id': 3}, {'titulo': u'Rambo', u'id': 5}, {'titulo': u'Rambo 2', u'id': 6}, {'titulo': u'Curtindo a Vida Adoidado', u'id': 7}]>

  >>> Filme.objects.values_list()
  <QuerySet [(3, u'Batman'), (5, u'Rambo'), (6, u'Rambo 2'), (7, u'Curtindo a Vida Adoidado')]>
  >>> Filme.objects.values_list('id', flat=True)
  <QuerySet [3, 5, 6, 7]>

  >>> Sessao.objects.select_related('sala__cinema')
  <QuerySet [<Sessao: Sessao object>, <Sessao: Sessao object>]>
  >>> str(Sessao.objects.select_related('sala__cinema').query)
  'SELECT "cinema_sessao"."id", "cinema_sessao"."sala_id", "cinema_sessao"."filme_id", "cinema_sessao"."inicio", "cinema_sessao"."fim", "cinema_sala"."id", "cinema_sala"."nome", "cinema_sala"."cinema_id", "cinema_cinema"."id", "cinema_cinema"."nome", "cinema_cinema"."cidade_id" FROM "cinema_sessao" INNER JOIN "cinema_sala" ON ("cinema_sessao"."sala_id" = "cinema_sala"."id") INNER JOIN "cinema_cinema" ON ("cinema_sala"."cinema_id" = "cinema_cinema"."id")'

  >>> Filme.objects.prefetch_related('sessoes__sala__cinema')
  <QuerySet [<Filme: Batman>, <Filme: Rambo>, <Filme: Rambo 2>, <Filme: Curtindo a Vida Adoidado>]>
  >>> str(Filme.objects.prefetch_related('sessoes__sala__cinema').query)
  'SELECT "cinema_filme"."id", "cinema_filme"."titulo" FROM "cinema_filme"'
  >>> str(Filme.objects.prefetch_related('sessoes__sala__cinema').filter(sessoes__sala__cinema__nome='Cinemark').query)
  'SELECT "cinema_filme"."id", "cinema_filme"."titulo" FROM "cinema_filme" INNER JOIN "cinema_sessao" ON ("cinema_filme"."id" = "cinema_sessao"."filme_id") INNER JOIN "cinema_sala" ON ("cinema_sessao"."sala_id" = "cinema_sala"."id") INNER JOIN "cinema_cinema" ON ("cinema_sala"."cinema_id" = "cinema_cinema"."id") WHERE "cinema_cinema"."nome" = Cinemark'


----

Métodos que realizam consultas no banco
=======================================

2) Métodos que não retornam querysets

- ``iterator``
- ``exists``
- ``count``
- ``aggregate``

.. code:: python

  >>> Filme.objects.iterator()
  <generator object __iter__ at 0x7f7d4b6479b0>

  >>> Filme.objects.exists()
  True

  >>> Filme.objects.count()
  4

  >>> from django.db.models import Max
  >>> Filme.objects.aggregate(Max('titulo'))
  {'titulo__max': u'Rambo 2'}


----

Customizando Querysets
======================

Criando uma classe de ``QuerySet`` customizada, podemos criar métodos especiais para fazer consultas que podem ser reaproveitadas em diversos lugares do código.

.. code:: python

  class FilmeQuerySet(models.QuerySet):
      def da_cidade(self, nome_cidade):
          return self.filter(
              sessoes__sala__cinema__cidade__nome=nome_cidade
          )

      def do_cinema(self, nome_cinema):
          return self.filter(
              sessoes__sala__cinema__nome=nome_cinema
          )

      def de_hoje(self):
          return self.filter(sessoes__inicio__date=date.today())


  class FilmeManager(models.Manager):
      def get_queryset(self):
          return FilmeQuerySet(self.model, using=self._db)

      def da_cidade(self, nome_cidade):
          return self.get_queryset().da_cidade(nome_cidade)

      def do_cinema(self, nome_cinema):
          return self.get_queryset().do_cinema(nome_cinema)

      def de_hoje(self):
          return self.get_queryset().de_hoje()



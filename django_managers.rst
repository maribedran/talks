===============
Django Managers
===============


----


O Modelo
========

Um modelo no django é uma classe que representa uma entrada em uma tabela no banco de dados.

.. code:: python

  from django.db import models

  class Pessoa(models.Model):
    nome = models.CharField()


Uma instância do modelo representa apenas uma entrada no banco, para acessar e manipular conjuntos de entradas o django tem as classes de **managers**.


----


O Manager
=========

Todo modelo no django tem implicitamante uma manager que é acessado pelo atributo de classe ``objects``, ele é responsável por fazer a interface entre o modelo e as operações no banco. Podemos customizar o manager do nosso modelo criando uma classe que herde de ``models.Manager``

.. code:: python

  from django.db import models


  class PessoaManager(models.Manager):
    pass


  class Pessoa(models.Model):
    nome = models.CharField()

    objects = Pessoamanager()


----


Os métodos de manager
=====================

- Métodos que retornam instâncias do modelo.

.. code:: python

  >>> Pessoa.objects.get(nome='João')
  Pessoa.

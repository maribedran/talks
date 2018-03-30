# Explorando QuerySets do Django

---

@maribedran

[twitter.com/maribedran](https://twitter.com/maribedran)

[github.com/maribedran](https://github.com/maribedran)

[maribedran@gmail.com]()

---

## Conhecendo o Django

---

Documentação oficial

[docs.djangoproject.com](https://docs.djangoproject.com/)

---

Tutoria do Django Girls

[tutorial.djangogirls.org/pt/](https://tutorial.djangogirls.org/pt/)

---

## O que o Django faz com uma requisição?

1. WSGI é o ponto de entrada da aplicação
- Decide o que fazer com ela
2. Middlewares (segurança, sessões, autenticação etc.)
- `urls.py` faz o roteamento *
3. Devolve uma resposta HTTP
- `views.py` delega tarefas *
- Lógica de negócio *
* Validação de dados (`forms.py` ou `serializers.py`)  *
* Persistência (`models.py` - BD, arquivos locais ou remotos) *
* Formatação da resposta (**html**, json, xml, arquivo etc) *

---

## Arquivos padrão de uma app

1. `urls.py` faz o roteamento
2. `views.py` processa a requisição
3. `forms.py` (`serializers.py` no DRF) valida e formata dados
4. `models.py` persiste e recupera dados no banco <==

---

## Models, Managers e QuerySets

---

### O Modelo

    Um modelo no django é uma classe que define uma tabela no banco de dados.

Cada **atributo** do modelo representa uma **coluna** da tabela.
O tipo de campo declarado determina o tipo da coluna.

    Uma instância dessa classe representa uma entrada na tabela.

Cada **atributo** na instância representa o **valor** da linha que ela representa para a respectiva coluna

---

```
+------------------------------+
|           Pessoa             | <== classe
+------+----------+------------+
| id   | nome     | nascimento |
+------+----------+------------+
| 1    | Maria    | 01/05/1990 | <-- isntância
+------+----------+------------+
| 2    | João     | 30/10/2015 | <-- isntância
+------+----------+------------+
```

---

Modelo.

```
class Cinema(models.Model):
     nome = models.CharField(max_length=50)
     cidade = models.ForeignKey(Cidade)
```

SQL gerado pela migração.

```
CREATE TABLE "cinema_cinema" (
  "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  "nome" varchar(50) NOT NULL,
  "cidade_id" integer NOT NULL REFERENCES "cinema_cidade" ("id")
);
```

---

### O Managers

    Uma instância do modelo representa apenas uma entrada no banco, para acessar e manipular conjuntos de entradas o Django tem as classes de **Managers**.

```
Filme.objects.all()  # Retorna todos os filmes

```

---

Todo modelo no Django tem implicitamante uma Manager que é acessado pelo atributo de classe `objects`, ele é responsável por fazer a interface entre o modelo e as operações no banco.

```
class FilmeManager(models.Manager):
    pass


class Filme(models.Model):
    titulo = models.CharField(max_length=255)

    objects = FilmeManager()
```

Podemos customizar o manager do nosso modelo criando uma classe que herde de `models.Manager`


---

### O QuerySet

  As tarefas de consulta no banco realizadas pelos managers são chamadas ao **QuerySet** do modelo, uma classe que herda de `models.QuerySet` e pode ser customizada da mesma forma que se faz com o manager.

Um objeto QuerySet é um iterável e seus elementos são instâncias do modelo ou objetos python simples.

---

Os métodos de consulta no banco que usamos do atributo `objects`, como `all` e `filter`, retornam chamadas de métodos com o mesmo nome do QuerySet.

```
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

```

---

## As entidades da nossa aplicação

Para dar um pouco de contexto, vamos usar uma aplicação que registra a programação de cinemas em diferentes cidades.

```
GENEROS = (
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
```

---

```
class Cidade(models.Model):
    nome = models.CharField('Cidade', max_length=50)

    def __str__(self):
        return self.nome


class Cinema(models.Model):
    nome = models.CharField('Nome', max_length=50)
    cidade = models.ForeignKey(Cidade, related_name='cinemas', on_delete=models.CASCADE)

    def __str__(self):
        return self.nome
```

---


```
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
```

---

```
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
```

---

## Os métodos de manager

### Métodos que retornam instâncias do modelo

- `get(**kwargs)`

```
SELECT ... FROM ... table WHERE ... ;
```

- `first()`

```
SELECT ... FROM ... table ORDER BY ... ASC LIMIT 1;
```

- `last()`

```
SELECT ... FROM ... table ORDER BY .. DESC LIMIT 1;
```

- `earliest(arg)`

```
SELECT ... FROM ... table ORDER BY ... ASC LIMIT 1;
```

- `latest(arg)`

```
SELECT ... FROM ... table ORDER BY .. DESC LIMIT 1;
```

**Atenção!**

`get` levanta a exceção `models.MultipleObjectsReturned` se encontrar mais de uma entrada e `models.DoesNotExist` se não encontrar nenhuma.

Os demais retornam `None` se não houver entradas correspondentes.

---

```
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
```

---

### Métodos que criam, atualizam e deletam

- `create(**kwargs)`

```
INSERT INTO table (...) VALUES (...);
```

- `update(**kwargs)`

```
UPDATE table SET <FIELD> = <VALUE>, ...;
```

- `get_or_create(**kwargs)`

```
SELECT ... FROM ... table WHERE ... ;
??? INSERT INTO table (...) VALUES (...);
```

- `update_or_create(defaults={...}, **kwargs)`

```
SELECT ... FROM ... table WHERE ...;
??? UPDATE table SET <FIELD> = <VALUE>, ... WHERE ...;
??? INSERT INTO table (...) VALUES (...);
```

- `bulk_create`

```
```

- `delete`

```
```

---

```
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
```

---

### Métodos que retornam QuerySets

Filtros

- `all()`: `SELECT ... FROM ... table`
- `none()`: não acessa o banco
- `filter(**kwargs)`: `SELECT ... FROM table WHERE ...`
- `exclude(**kwargs)`: `SELECT ... FROM table WHERE NOT ...`
- `distinct()`: `SELECT DISTINCT ... FROM ... table`

---

### Métodos que retornam QuerySets

Ordenação

- `order_by(arg)`: `SELECT ... FROM ... table ORDER BY ...`
- `order_by(arg).reverse()` ou `order_by('-ARG')`: `SELECT ... FROM ... table ORDER BY DESC...`


---

### Métodos que retornam QuerySets

Valores

- `values(**kargs)`: `SELECT <FIELDS> FROM ... table`
* Seleciona todos se não receber argumentos
* Retorna um QuerySet com dicts
- `values_list` `SELECT ... FROM ... table`
*
- `only` `SELECT ... FROM ... table`

- `defer` `SELECT ... FROM ... table`


---

### Métodos que retornam QuerySets

Relações com outras tabelas
- `select_related`
- `prefetch_related`

---

```
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

>>> Filme.objects.reverse()
<QuerySet [<Filme: Batman>, <Filme: Rambo>, <Filme: Rambo 2>, <Filme: Curtindo a Vida Adoidado>]>

>>> Filme.objects.distinct()
<QuerySet [<Filme: Batman>, <Filme: Rambo>, <Filme: Rambo 2>, <Filme: Curtindo a Vida Adoidado>]>
```

---

```
>>> Filme.objects.annotate(salas=F('sessoes__sala__nome'))
<QuerySet [<Filme: Batman>, <Filme: Rambo>, <Filme: Rambo 2>, <Filme: Curtindo a Vida Adoidado>]>

>>> Filme.objects.annotate(salas=F('sessoes__sala__nome')).first().salas
u'1'

>>> Filme.objects.values()
<QuerySet [{'titulo': u'Batman', u'id': 3}, {'titulo': u'Rambo', u'id': 5}, {'titulo': u'Rambo 2',
u'id': 6}, {'titulo': u'Curtindo a Vida Adoidado', u'id': 7}]>

>>> Filme.objects.values_list()
<QuerySet [(3, u'Batman'), (5, u'Rambo'), (6, u'Rambo 2'), (7, u'Curtindo a Vida Adoidado')]>

>>> Filme.objects.values_list('id', flat=True)
<QuerySet [3, 5, 6, 7]>
```

---


```
>>> Sessao.objects.select_related('sala__cinema')
<QuerySet [<Sessao: Sessao object>, <Sessao: Sessao object>]>

>>> str(Sessao.objects.select_related('sala__cinema').query)
'SELECT "cinema_sessao"."id", "cinema_sessao"."sala_id", "cinema_sessao"."filme_id", "cinema_sessao".
"inicio", "cinema_sessao"."fim", "cinema_sala"."id", "cinema_sala"."nome", "cinema_sala"."cinema_id",
"cinema_cinema"."id", "cinema_cinema"."nome", "cinema_cinema"."cidade_id" FROM "cinema_sessao" INNER
JOIN "cinema_sala" ON ("cinema_sessao"."sala_id" = "cinema_sala"."id") INNER JOIN "cinema_cinema" ON
("cinema_sala"."cinema_id" = "cinema_cinema"."id")'
```

---

```
>>> Filme.objects.prefetch_related('sessoes__sala__cinema')
<QuerySet [<Filme: Batman>, <Filme: Rambo>, <Filme: Rambo 2>, <Filme: Curtindo a Vida Adoidado>]>

>>> str(Filme.objects.prefetch_related('sessoes__sala__cinema').query)
'SELECT "cinema_filme"."id", "cinema_filme"."titulo" FROM "cinema_filme"'

>>> str(Filme.objects.prefetch_related('sessoes__sala__cinema').filter(sessoes__sala__cinema__nome
='Cinemark').query)
'SELECT "cinema_filme"."id", "cinema_filme"."titulo" FROM "cinema_filme" INNER JOIN "cinema_sessao"
ON ("cinema_filme"."id" = "cinema_sessao"."filme_id") INNER JOIN "cinema_sala" ON ("cinema_sessao".
"sala_id" = "cinema_sala"."id") INNER JOIN "cinema_cinema" ON ("cinema_sala"."cinema_id" = "cinema_
cinema"."id") WHERE "cinema_cinema"."nome" = Cinemark'
```

---

> Todos os métodos que retornam querysets podem ter chamadas encadeadas e a execução deles é *lazzy*, ou seja, é possível chamar vários métodos que fazem queries diferentes, mas que só serão executadas uma vez.

---

Métodos que realizam consultas no banco e não retornam querysets

- ``iterator``
- ``exists``
- ``count``
- ``aggregate``


---

```
>>> Filme.objects.iterator()
<generator object __iter__ at 0x7f7d4b6479b0>

>>> Filme.objects.exists()
True

>>> Filme.objects.count()
4

>>> from django.db.models import Max
>>> Filme.objects.aggregate(Max('titulo'))
{'titulo__max': u'Rambo 2'}
```

---

## Customizando Querysets

> Criando uma classe de ``QuerySet`` customizada, podemos criar métodos especiais para fazer consultas que podem ser reaproveitadas em diversos lugares do código.


---

```
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
```

---

```
class SessaoQuerySet(models.QuerySet):
    def do_filme(self, nome_filme):
        return self.filter(filme__titulo__contains=nome_filme)

    def da_cidade(self, nome_cidade):
        return self.filter(sala__cinema__cidade__nome__contains=nome_cidade)

    def do_cinema(self, nome_cinema):
        return self.filter(sala__cinema__nome__contains=nome_cinema)

    def de_hoje(self):
        return self.filter(inicio__date=date.today())

```

---

```
    def lotadas(self):
        return self.annotate(
            ocupacao=Count('ingressos')
        ).filter(sala__lotacao__lte=F('ocupacao'))

    def livres(self):
        return self.annotate(
            ocupacao=Count('ingressos')
        ).filter(sala__lotacao__gte=F('ocupacao'))

```

---

> That's all folks!

[github.com/maribedran/talks/](https://github.com/maribedran)


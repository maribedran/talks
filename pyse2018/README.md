# Explorando QuerySets do Django

Palestra apresentada em 2018 na Python Sudeste em São Paulo e na Python Sul em Florianópolis.

---

@maribedran

[twitter.com](https://twitter.com/maribedran)

[github.com](https://github.com/maribedran)

[gmail.com]()

---

## Conhecendo o Django

---

Documentação oficial

[docs.djangoproject.com](https://docs.djangoproject.com/)


Tutoria do Django Girls

[tutorial.djangogirls.org/pt/](https://tutorial.djangogirls.org/pt/)

---

## Aprendendo SQL através do Django

Para quem não conhece SQL a ORM pode ser uma ferramenta de aprendizagem.

Leia as queries que estão sendo realizadas e experimente rodá-las direto no banco. A sintaxe do SQL é simples e intuitiva, em pouco tempo você aprende o básico.

Observe a quantidade de queries sendo feitas e o tempo que elas demoram.

---

Ative os logs em nível DEBUG nos settings.

```
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',    # Loga no terminal
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',                    # Exibe todas as queries
        },
    },
}
```

---

Instale o Django Debug Toolbar

[django-debug-toolbar.readthedocs.io](django-debug-toolbar.readthedocs.io)

Para funcionar com o Rest Framework, adicione esta configuração aos settings.

```
DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda x: True,
}
```

---

## Bancos de dados relacionais

Em um banco relacional os dados são organizados em tabelas em que cada coluna define o nome e o tipo do campo que vai ser armazenado.

As colunas que criam relações entre as tabelas são as chaves estrangeiras, onde uma entrada é uma referência a uma linha de outra tabela.

---


```
+------------------------------+            +-------------------+
|           Pessoa             |            |   Empresa         |
+------+----------+------------+            +------+------------+
| id   | nome     | empresa_id |            | id   | nome       |
+------+----------+------------+            +------+------------+
| 1    | Maria    | 2          | ---------> | 2    | Empresa SA |
+------+----------+------------+            +------+------------+
| 2    | João     | 4          | ---------> | 4    | Company    |
+------+----------+------------+            +------+------------+

```

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

Modelo.

```
class Cinema(models.Model):
    nome = models.CharField('Nome', max_length=50)
    cidade = models.ForeignKey(Cidade, related_name='cinemas', on_delete=models.CASCADE)

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

#### Responsabilidades

Uma instância do modelo representa apenas uma entrada individual no banco, portanto os métodos de instância deveriam realizar somente operações que afetam um objeto individual.

---

1. Properties que retornam atributos da entidade ou de objetos relacionados

```

class Ingresso(models.Model):
    ...

    @property
    def preco(self):
        return self.sessao.preco / 2 if self.meia_entrada else self.sessao.preco
```

---

2. Métodos que verificam estados e garantem sua integridade

```

class Sessao(models.Model):
    ...

    @property
    def ocupacao(self):
        return self.ingressos.count()

    @property
    def lotada(self):
        return self.lotacao <= self.ocupacao

    @property
    def aberta_para_venda(self):
        return self.inicio - timedelta(minutes=10) >= datetime.now()

    def verificar_disponibilidade(self):
      assert not self.lotada and self.aberta_para_venda

```

---

### O Managers

Para acessar e manipular conjuntos de entradas o Django tem as classes de **Managers**.

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

#### Responsabilidades

Criar, atualizar e remover entradas no banco.

```
class UserManager(BaseUserManager):
    ...

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)
```

---

### O QuerySet

O  **QuerySet** do modelo é uma classe que herda de `models.QuerySet` e pode ser customizada da mesma forma que se faz com o manager.

As tarefas de consulta no banco realizadas pelos managers são chamadas ao QuerySet do modelo.

Um objeto QuerySet é um iterável e seus elementos são instâncias do modelo ou objetos python simples.

---

Os métodos de consulta no banco que usamos do atributo `objects`, como `all` e `filter`, retornam chamadas de métodos com o mesmo nome do QuerySet.

```
class FilmeQuerySet(models.QuerySet):
    
    def de_acao(self, *args, **kwargs):
        return self.filter(genero='ACAO')

class FilmeManager(models.Manager):
    def get_queryset(self):
        return FilmeQuerySet(self.model, using=self._db)

    def de_acao(self, *args, **kwargs):
        return self.get_queryset().de_acao(*args, **kwargs)

```

---

#### Responsabilidades

Realizar consultas no banco abstraindo os detalhes de implementação para o resto da aplicação.


```
class FilmeQuerySet(models.QuerySet):
    
    def de_acao(self, *args, **kwargs):
        return self.filter(genero='ACAO')

```

---

## As entidades da nossa aplicação

Para dar um pouco de contexto, vamos usar uma aplicação que registra a programação de cinemas em diferentes cidades.

---

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

## Os métodos de Managers e QuerySets

---

### Métodos que retornam instâncias do modelo

---

- `get(id=10, nome='Maria')`

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

- `earliest('nome')`

```
SELECT ... FROM ... table ORDER BY ... ASC LIMIT 1;
```

- `latest('nome')`

```
SELECT ... FROM ... table ORDER BY .. DESC LIMIT 1;
```

---

**Atenção!**

`get` levanta a exceção `models.MultipleObjectsReturned` se encontrar mais de uma entrada e `models.DoesNotExist` se não encontrar nenhuma.

Os demais retornam `None` se não houver entradas correspondentes.

---

### Métodos que criam, atualizam e deletam

---

- `create(nome='Maria')`

```
INSERT INTO table (...) VALUES (...);
```

- `update(nome='Maria')`

```
UPDATE table SET <FIELD> = <VALUE>, ...;
```

- `bulk_create([Pessoa(nome='Maria'), Pessoa(nome='João')])`

```
INSERT INTO table (<FIELDS>) SELECT ... UNION ALL SELECT ...;
```

---

- `get_or_create(nome='Maria')`

```
SELECT ... FROM ... table WHERE ... ;
??? INSERT INTO table (...) VALUES (...);
```

- `update_or_create(defaults={'idade': 30}, nome='Maria')`

```
SELECT ... FROM ... table WHERE ...;
??? UPDATE table SET <FIELD> = <VALUE>, ... WHERE ...;
??? INSERT INTO table (...) VALUES (...);
```


- `delete()`

```
DELETE FROM table WHERE ...;
```

---

### Métodos que retornam QuerySets

---

- `all()`

```
SELECT ... FROM ... table
```

- `none()`

não acessa o banco

- `filter(nome='Maria')`

```
SELECT ... FROM table WHERE ...
```

- `exclude(nome='Maria')`

```
SELECT ... FROM table WHERE NOT ...
```

- `distinct()`

```
SELECT DISTINCT ... FROM ... table
```

---


- `order_by('nome')`

```
SELECT ... FROM ... table ORDER BY ...
```

- `order_by(arg).reverse()` ou `order_by('-ARG')`

```
SELECT ... FROM ... table ORDER BY DESC...
```


---


- `values('nome')`

```
SELECT ... FROM table
```

Seleciona todos se não receber argumentos
Retorna um QuerySet com dicts

- `values_list('nome')`

```
SELECT ... FROM table
```

Retorna um QuerySet com tuplas de valores

---

- `only('nome')`

```
SELECT ... FROM table
```

- `defer('nome')`

```
SELECT ... FROM table
```


---


- `select_related('filme')`

```
SELECT ... FROM table
INNER JOIN table2 ON table.table2_id = table2.id
```

- `prefetch_related('ingressos')`

```
SELECT ... FROM table
SELECT ... FROM table2 WHERE table2.table_id IN …
```

---

Todos os métodos que retornam querysets podem ter chamadas encadeadas e a execução deles é *lazzy*, ou seja, é possível chamar vários métodos que fazem queries diferentes, mas que só serão executadas uma vez.

---

Métodos que realizam consultas no banco e não retornam querysets

- `iterator()`

```
SELECT ... FROM table;
```

Retorna um objeto gerador
Só realiza a query quando o primeiro elemento é acessado

- `exists()`

```
SELECT (1) AS "a" FROM table LIMIT 1;
```

Retorna um booleano

- `count()`

```
SELECT COUNT(*) AS "__count" FROM table;
```

Retorna um inteiro

- `aggregate(expression)`

```
SELECT <EXPRESSIO> AS <ALIAS> FROM table;
```

Retorna um dict com o valor da expressão

---

## Customizando Querysets

Criando uma classe de ``QuerySet`` customizada, podemos criar métodos especiais para fazer consultas que podem ser reaproveitadas em diversos lugares do código.

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

### Usando QuerySets de forma eficienteno projeto

---

```
class FilmeFilter(FilterSet):
    da_cidade = django_filters.CharFilter(label='Da Cidade', method='filter_da_cidade')
    do_cinema = django_filters.CharFilter(label='Do Cinema', method='filter_do_cinema')
    de_hoje = django_filters.BooleanFilter(label='De Hoje', method='filter_de_hoje')

    class Meta:
        model = Filme
        fields = ['titulo', 'genero', 'da_cidade', 'do_cinema', 'de_hoje']

    def filter_da_cidade(self, queryset, name, value):
        return queryset.da_cidade(value)

    def filter_do_cinema(self, queryset, name, value):
        return queryset.do_cinema(value)

    def filter_de_hoje(self, queryset, name, value):
        if value:
            return queryset.de_hoje()
        return queryset
```

---

```
class Sessao(models.Model):
    ...

    @property
    def ocupacao(self):
        return self.ingressos.count()


class SessaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sessao
        fields = ('id', 'sala', 'filme', 'inicio', 'fim', 'preco', 'ocupacao', )


class SessaoViewSet(ModelViewSet):
    queryset = Sessao.objects.prefetch_related('ingressos')
    serializer_class = SessaoSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = SessaoFilter
```
---
> That's all folks!

[github.com/maribedran/talks/](https://github.com/maribedran)


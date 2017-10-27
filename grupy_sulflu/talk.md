# Django

O framework web mais completo que você respeita

---

# Olar

@maribedran

[twitter.com/maribedran](https://twitter.com/maribedran)

[github.com/maribedran](https://github.com/maribedran)

[maribedran@gmail.com]()

@WPensar SA

---

## Conhecendo o Django

- Documentação oficial

    [docs.djangoproject.com](https://docs.djangoproject.com/)

- Tutoria do Django Girls

    [tutorial.djangogirls.org/pt/](https://tutorial.djangogirls.org/pt/)


---

## Internet


    https://google.com          [A Internet]          8.8.8.8

        +-----+                 HTTP Request           +----+
        |     |             ------------------>        |    |
        +-----+                                        |    |
        -------             <------------------        +----+
        -------                 HTTP Response

---

    "Uma aplicação web é um software que sabe processar uma requisição e retornar uma resposta para ela."


![Browser request](images/django_docs_request.png)


---

## O que tem em uma aplicação web?

```
                                Servidor
                  +----------------------------------+
                  |   Aplicações                     |
                  |    _   _                         |
                  |   |_| |_| ----->   +----------+  |
        Internet  |                    | Arquivos |  |
                  |    ______          |    BD    |  |
                  |   |Django| ---->   +----------+  |
                  |   +------+                       |
                  +----------------------------------+

```

---

## Tarefas básicas de uma aplicação

---

1. Receber uma requisição
    * WSGI conversa com o servidor
2. Decidir o que fazer com ela
    * Roteamento `urls.py`
3. Enviar uma resposta
    * Lógica de negócio implementada (seu código python)
    * Persistência (BD, arquivos locais, arquivos remotos)
    * Formatação da resposta pra quem vai consumi-la (json, html, css, js, xml, arquivo)

---

## O Django cuida de quase tudo pra você


```
             ===========  Django ==========
            ||                            ||
            \/                            \/
        +-----------------------------------------+
        |               |        |                |
        |               |        |                |
        |  Apresentação | Lógica |  Persistência  |
        |               |        |                |
        |               |        |                |
        +-----------------------------------------+
            /\              /\
            ||              ||
            ====== Você =====


```

---

## O padrão **M**odel**V**iew**T**emplate
A gente só mexe aqui

```
     +-----------------+
     |     urls.py     | Roteamento
     +-----------------+
             \/
     +-----------------+                    +-------------+
     |     views.py    | Delega tarefas ==> |  Templates  |
     +-----------------+                    +-------------+
             \/
     +-----------------+
     |     forms.py    | Validação e formatação de dados
     +-----------------+
             \/
     +-----------------+                     +----+
     |    models.py    |  Persistência   ==> | DB |
     +-----------------+                     +----+

```

---

## Começando um projeto

    $ pip install django==1.11           # Instalando o Django
    $ django-admin startproject project  # Inicializando o projeto
    $ cd project/
    $ python manage.py startapp cinema   # Criando um app

---

## Estrutura do projeto

     ▾ project/
       ▾ cinema/
         ▾ migrations/
             __init__.py
           __init__.py
           admin.py
           apps.py
           models.py
           tests.py
           views.py
       ▾ project/
         ▾ __pycache__/
           __init__.py
           settings.py
           urls.py
           wsgi.py
         manage.py*

---

## manage.py

```shell

    $ python manage.py --help

    Type 'manage.py help <subcommand>' for help on a specific subcommand.

    Available subcommands:

    [auth]
        changepassword
        createsuperuser

    [contenttypes]
        remove_stale_contenttypes

    [django]
        check
        compilemessages
        createcachetable
        dbshell
        diffsettings
        dumpdata
        flush
        inspectdb
        loaddata
        makemessages
        makemigrations
        migrate
        sendtestemail
        shell
        showmigrations
        sqlflush
        sqlmigrate
        sqlsequencereset
        squashmigrations
        startapp
        startproject
        test
        testserver

    [sessions]
        clearsessions

    [staticfiles]
        collectstatic
        findstatic
        runserver

```


---

## Migrando o banco

```
    $ python manage.py migrate
    Operations to perform:
      Apply all migrations: admin, auth, contenttypes, sessions
    Running migrations:
      Applying contenttypes.0001_initial... OK
      Applying auth.0001_initial... OK
      Applying admin.0001_initial... OK
      Applying admin.0002_logentry_remove_auto_add... OK
      Applying contenttypes.0002_remove_content_type_name... OK
      Applying auth.0002_alter_permission_name_max_length... OK
      Applying auth.0003_alter_user_email_max_length... OK
      Applying auth.0004_alter_user_username_opts... OK
      Applying auth.0005_alter_user_last_login_null... OK
      Applying auth.0006_require_contenttypes_0002... OK
      Applying auth.0007_alter_validators_add_error_messages... OK
      Applying auth.0008_alter_user_username_max_length... OK
      Applying sessions.0001_initial... OK
```

---

## Rodando o servidor


```
    $ python manage.py runserver
    Performing system checks...

    System check identified no issues (0 silenced).
    October 25, 2017 - 22:27:55
    Django version 1.11, using settings 'project.settings'
    Starting development server at http://127.0.0.1:8000/
    Quit the server with CONTROL-C.

```

---

## Pronto! É realmente só isso!

![It worked](images/it_worked.png)

![Admin](images/admin.png)

---

## Adicionando nossa app

`project/setting.py`

```

    # Application definition

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'cinema',
    ]

```

---

## Tudo configurado!

Bora implementar a app!

---

## urls.py

Onde configuramos nossas rotas.


```
    # project/urls.py

    from django.conf.urls import url
    from django.contrib import admin

    urlpatterns = [
        url(r'^admin/', admin.site.urls),
    ]

```

---

## Retornando conteúdo

```
    # project/urls.py

    from django.conf.urls import url
    from django.contrib import admin
    from django.http import HttpResponse

    urlpatterns = [
        url(r'^admin/', admin.site.urls),
        url(r'^$', lambda request: HttpResponse('<h1>Olar!</h1>')),
    ]

```

---

>   Uma view é só uma função que recebe um objeto `HttpRequest` e retorna um `HttpResponse`.

```
    url(r'^$', lambda request: HttpResponse('<h1>Olar!</h1>'))

         /\               /\
         ||               ||
        rota             view
```

---

## Renderizando templates


```
texto = """
<h1>Classe de template: {{ template_class }}</h1>
<h1>Classe de Contexto: {{ context_class }}</h1>
"""
template = Template(texto)
contexto = {
    "template_class": str(Template),
    "context_class": str(Context)
}

urlpatterns = [
    url(r'^templates/$', lambda request: HttpResponse(
            template.render(Context(contexto)))),
]

```

---

## Fazendo todas as operações de CRUD

> **C**reate**R**etrieve**U**pdate**D**elete

---


`projec/urls.py`

```
    url(r'^cinema', include('cinema.urls')),
```

`cinema/urls.py`

```
urlpatterns = [
    url(r'^/$',
        FilmeListView.as_view(), name='filme-list'),
    url(r'^/criar/$',
        FilmeCreateView.as_view(), name='filme-create'),
    url(r'^/(?P<pk>[0-9]+)/$',
        FilmeDetailView.as_view(), name='filme-detail'),
    url(r'^/(?P<pk>[0-9]+)/editar/$',
        FilmeUpdateView.as_view(), name='filme-update'),
    url(r'^/(?P<pk>[0-9]+)/remover/$',
        FilmeDeleteView.as_view(), name='filme-delete'),
]

```

---

`cinema/views.py`


```
from django.views.generic import (
    ListView, DetailView, CreateView,
    UpdateView, DeleteView
)
from django.urls import reverse_lazy
from cinema.models import Filme


class FilmeListView(ListView):
    model = Filme


class FilmeDetailView(DetailView):
    model = Filme

```

---

`cinema/views.py`

```
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
```

---

## Templates

> O Django espertamente encontra os templates pelo nome.

```
 ▾ cinema/
   ▸ migrations/
   ▾ templates/cinema/
       filme_confirm_delete.html
       filme_detail.html
       filme_form.html
       filme_list.html
     __init__.py
     admin.py
     apps.py
     models.py
     tests.py
     urls.py
     views.py
```

---

`cinema/templates/cinema/filme_list.html`

```
<h1>Filmes em cartaz</h1>
<ul>
	{% for filme in object_list %}
		<li>{{ filme.titulo }}</li>
	{% endfor %}
</ul>
```

`cinema/templates/cinema/filme_detail.html`

```
<h1>{{ filme.titulo }}</h1>

```

---

`cinema/templates/cinema/filme_form.html`

```
{% if object %}
    Editar {{ object.titulo }}
{% else %}
    Novo Filme
{% endif %}
<form action="" method="post">
    {% csrf_token %}
    {{ form }}
    <input type="submit" value="Salvar" />
</form>
```

`cinema/templates/cinema/filme_delete.html`

```
<form action="" method="post">
    {% csrf_token %}
	Deseja remover o filme?
    <input type="submit" value="Sim" />
</form>
```

---

## Manipulando dados de forma simples e eficiente

### 1. Modelo
### 2. Manager
### 3. QuerySet

---

## 1. O Modelo

> Um modelo no django é uma classe que representa uma entrada em uma tabela no banco de dados.

Cada atributo do modelo representa uma coluna da tabela e o tipo de campo declarado determina o tipo da coluna.

---

## 2. O Manager

> Uma instância do modelo representa apenas uma entrada no banco, para acessar e manipular conjuntos de entradas o django tem as classes de **managers**.

```
Filme.objects.all()  # Retorna todos os filmes

```

---

Todo modelo no django tem implicitamante uma manager que é acessado pelo atributo `objects`, ele é responsável por fazer a interface entre o modelo e as operações no banco.

```
class FilmeManager(models.Manager):
    pass


class Filme(models.Model):
    titulo = models.CharField(max_length=255)

    objects = FilmeManager()
```

Podemos customizar o manager do nosso modelo criando uma classe que herde de `models.Manager`


---

## O QuerySet

> As tarefas de consulta no banco realizadas pelos managers são chamadas a uma classe de `models.QuerySet`, que pode ser customizada da mesma forma que se faz com o manager.

Os métodos de consulta no banco que usamos do `objects` padrão do modelo,
  como `all` e `filter` retornam chamadas de métodos com o mesmo nome do
  `QuerySet` do modelo.

---

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

```
class Filme(models.Model):
    titulo = models.CharField(max_length=255)


class Cidade(models.Model):
    nome = models.CharField(max_length=50)


class Cinema(models.Model):
    nome = models.CharField(max_length=50)
    cidade = models.ForeignKey(Cidade)


```

---


```
class Sala(models.Model):
    nome = models.CharField(max_length=10)
    cinema = models.ForeignKey(Cinema, related_name='salas')
    lotacao = models.IntegerField()


class Sessao(models.Model):
    sala = models.ForeignKey(Sala, related_name='sessoes')
    filme = models.ForeignKey(Filme, related_name='sessoes')
    inicio = models.DateTimeField()
    fim = models.DateTimeField()


class Ingresso(models.Model):
    sessao = models.ForeignKey(Sessao, related_name='ingressos')
```

---

## Os métodos de manager

Métodos que retornam instâncias do modelo

- ``get``
- ``first``
- ``last``
- ``earliest``
- ``latest``

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

Métodos que criam, atualizam e deletam

- ``create``
- ``update``
- ``get_or_create``
- ``update_or_create``
- ``bulk_create``
- ``delete``

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

Métodos que retornam querysets

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


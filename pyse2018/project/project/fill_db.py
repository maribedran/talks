import random
from model_mommy import mommy

from cinema.models import *


def fill_db():
    filmes = [
        Filme(titulo='Dunkirk', genero='ACAO'),
        Filme(titulo='Guardiões da Galáxia Vol. 2', genero='AVENTURA'),
        Filme(titulo='Mulher Maravilha', genero='AVENTURA'),
        Filme(titulo='Planeta dos Macacos: A Guerra', genero='ACAO'),
        Filme(titulo='Homem-Aranha: De Volta ao Lar', genero='AVENTURA'),
        Filme(titulo='Corra!', genero='TERROR'),
        Filme(titulo='John Wick: Um Novo Dia para Matar', genero='ACAO'),
        Filme(titulo='Silêncio', genero='DRAMA'),
        Filme(titulo='Ao Cair da Noite', genero='TERROR'),
    ]
    Filme.objects.bulk_create(filmes)

    cidades = [
        Cidade(nome='Rio de Janeiro'),
        Cidade(nome='São Paulo'),
        Cidade(nome='Recife'),
    ]
    Cidade.objects.bulk_create(cidades)

    nomes_cinemas = ['Do Bairro', 'Do Shopping', 'Cult']

    cidades = Cidade.objects.all()
    cinemas = [
        Cinema(nome=nome, cidade=cidade)
        for nome in nomes_cinemas for cidade in cidades
    ]
    Cinema.objects.bulk_create(cinemas)

    cinemas = Cinema.objects.all()
    salas = [
        Sala(cinema=cinema, lotacao=random.choice([30, 40, 50]), nome='Sala %d' % sala)
        for cinema in cinemas for sala in range(1, 6)
    ]
    Sala.objects.bulk_create(salas)

    horarios = [
        ('2018-04-06 16:00', '2018-04-06 17:40'),
        ('2018-04-06 18:00', '2018-04-06 19:40'),
        ('2018-04-06 20:00', '2018-04-06 21:40'),
        ('2018-04-06 22:00', '2018-04-06 23:40'),
    ]

    salas = Sala.objects.all()
    filmes = Filme.objects.all()
    sessoes = [
        Sessao(inicio=inicio, fim=fim, sala=sala, filme=random.choice(filmes), preco=random.choice([20, 30, 40]))
        for sala in salas for (inicio, fim) in horarios
    ]
    Sessao.objects.bulk_create(sessoes)

    sessoes = Sessao.objects.all()
    for i in range(800):
        mommy.make(Ingresso, sessao=random.choice(sessoes))

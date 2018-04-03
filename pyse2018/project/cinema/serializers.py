from rest_framework import serializers

from cinema.models import (
    Filme,
    Cidade,
    Cinema,
    Sala,
    Sessao,
    Ingresso,
)


class FilmeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filme
        fields = '__all__'


class CidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cidade
        fields = '__all__'


class CinemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cinema
        fields = '__all__'


class SalaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sala
        fields = '__all__'


class SessaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sessao
        fields = '__all__'


class IngressoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingresso
        fields = '__all__'


from django.db import models


class Filme(models.Model):
    titulo = models.CharField(max_length=255)


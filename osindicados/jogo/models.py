# -*- coding: utf-8 -*-
from django.db import models

DIFICULDADES = (
                    (1, 'fácil'),
                    (2, 'médio'),
                    (3, 'difícil'),
                    (4, 'desafio')
                )

class Tema(models.Model):
    nome = models.CharField(max_length=30)
    nomeTrofeu = models.CharField(max_length=30)
    imagemTrofeu = models.CharField(max_length=100)
    def __unicode__(self):
        return self.nome

class Pergunta(models.Model):
    enunciado = models.CharField(max_length=1000)
    altCorreta = models.CharField(max_length=200)
    altIncorreta1 = models.CharField(max_length=200)
    altIncorreta2 = models.CharField(max_length=200)
    altIncorreta3 = models.CharField(max_length=200)
    altIncorreta4 = models.CharField(max_length=200)
    dificuldade = models.IntegerField(choices=DIFICULDADES)
    idAssunto = models.ForeignKey(Tema)
    def __unicode__(self):
        return self.enunciado

class Placar(models.Model):
    nomeJogador = models.CharField(max_length=30)
    dificuldade = models.IntegerField(choices=DIFICULDADES)
    acertosEsporte = models.IntegerField()
    acertosCinema = models.IntegerField()
    acertosMusica = models.IntegerField()
    acertosTelevisao = models.IntegerField()
    acertosCGerais = models.IntegerField()
    acertosCiencias = models.IntegerField()
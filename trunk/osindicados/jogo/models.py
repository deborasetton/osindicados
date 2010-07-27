# -*- coding: utf-8 -*-
from django.db import models

DIFICULDADES = (
                    (1, 'Amador'),
                    (2, 'Profissional'),
                    (3, 'Celebridade'),
                    (4, 'Ídolo')
                )

class Tema(models.Model):

    def __init__(self, *args, **kwargs):
        super(Tema, self).__init__(*args, **kwargs)

    nome = models.CharField(max_length=30)
    nomeTrofeu = models.CharField(max_length=30)
    imagemTrofeu = models.CharField(max_length=100)
    def __unicode__(self):
        return self.nome

class Pergunta(models.Model):

    def __init__(self, *args, **kwargs):
        super(Pergunta, self).__init__(*args, **kwargs)

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

    @staticmethod
    def getPerguntaPorAssunto(assuntos, ids=[]):
        return Pergunta.objects.filter(idAssunto__nome__in=assuntos).exclude(id__in=ids).order_by('?')[:1][0]

    @staticmethod
    def getPerguntaPorIdsAssunto(idsAssunto, ids=[]):
        return Pergunta.objects.filter(idAssunto__in=idsAssunto).exclude(id__in=ids).order_by('?')[:1][0]

    @staticmethod
    def getPerguntasPartidaPorAssunto(assuntosPartida):
        return Pergunta.objects.filter(idAssunto__nome__in=assuntosPartida).order_by('?')[:25]

    @staticmethod
    def getPerguntasPartidaPorIdsAssunto(idsAssunto):
        return Pergunta.objects.filter(idAssunto__in=idsAssunto).order_by('?')[:25]

class Placar(models.Model):

    def __init__(self, *args, **kwargs):
        super(Placar, self).__init__(*args, **kwargs)
        if self.acertosEsporte is None:
            self.acertosEsporte = 0
        if self.acertosCinema is None:
            self.acertosCinema = 0
        if self.acertosMusica is None:
            self.acertosMusica = 0
        if self.acertosTelevisao is None:
            self.acertosTelevisao = 0
        if self.acertosCGerais is None:
            self.acertosCGerais = 0
        if self.acertosCiencias is None:
            self.acertosCiencias = 0
        
    nomeJogador = models.CharField(max_length=30)
    dificuldade = models.IntegerField(choices=DIFICULDADES)
    acertosEsporte = models.IntegerField()
    acertosCinema = models.IntegerField()
    acertosMusica = models.IntegerField()
    acertosTelevisao = models.IntegerField()
    acertosCGerais = models.IntegerField()
    acertosCiencias = models.IntegerField()

    def __unicode__(self):
        pontos = {'Esporte' : self.acertosEsporte,
                'Cinema' : self.acertosCinema,
                'Musica' : self.acertosMusica,
                'Televisao' : self.acertosTelevisao,
                'CGerais' : self.acertosCGerais,
                'Ciencias' : self.acertosCiencias,
                'Jogador' : self.nomeJogador,
                'Dificuldade' : self.dificuldade }
        return str(pontos)

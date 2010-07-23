# -*- coding: utf-8 -*-
import random
from osindicados.jogo.models import Placar

def sortearAlternativas(pergunta):
    alternativas = [pergunta.altCorreta, pergunta.altIncorreta1, pergunta.altIncorreta2, pergunta.altIncorreta3, pergunta.altIncorreta4]
    random.shuffle(alternativas)
    return alternativas

def temasPlacar(tema):
    if tema == u'Esporte': return 'acertosEsporte'
    elif tema == u'Cinema': return 'acertosCinema'
    elif tema == u'Música': return 'acertosMusica'
    elif tema == u'Televisão': return 'acertosTelevisao'
    elif tema == u'Conhecimentos Gerais': return 'acertosCGerais'
    elif tema == u'Ciências': return 'acertosCiencias'
    else: return 0
    
def selectPlacares(listaDeTemas):
    query = """SELECT id
                      ,nomeJogador
                      ,dificuldade
                      ,acertosEsporte
                      ,acertosCinema
                      ,acertosMusica
                      ,acertosTelevisao
                      ,acertosCGerais
                      ,acertosCiencias"""
                      
    if(listaDeTemas.__len__ > 0):
        query += ',(' + temasPlacar(listaDeTemas[0])
        for n in range(1, listaDeTemas.__len__()):
            query += ' + ' + temasPlacar(listaDeTemas[n])  
        query += ') AS total '
        
    query += """FROM jogo_placar
            ORDER BY Total DESC"""
    placares=[]
    for placar in Placar.objects.raw(query):
        placares.append(placar)
    
    return placares
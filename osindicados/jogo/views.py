# -*- coding: utf-8 -*-
from osindicados.jogo.models import Tema, Pergunta
from osindicados.jogo.partidaconfs import *
from django.shortcuts import render_to_response
from django.core.context_processors import request
from django.http import HttpResponse

def index(request):
    temas = Tema.objects.all()
    perguntas = Pergunta.objects.all()

    # calcula quantas perguntas foram cadastradas em cada tema
    list_tema_qntd = [(tema, len(Pergunta.objects.filter(idAssunto__exact=tema.id))) for tema in temas]

    return render_to_response('jogo/index.html', {'list_tema_qntd': list_tema_qntd, 'perguntas': perguntas})

def partida(request):
    print "Entrou no partida!"
    
    
    
    
    return render_to_response('jogo/partida.html', {'confs': request.session['confs']})

def config(request):
    # Mock para as opções do usuário
    dificuldade = 2
    temas = ['Cinema', 'Musica']
    # Cria um novo objeto passando as opções do usuário
    conf = Partidaconfs(dificuldade, temas)
    # Coloca na sessão
    request.session['confs'] = conf
    return render_to_response('jogo/config.html')

def responder(request):
    """
    Vem para cá quando o usuário responde uma pergunta.
    O request deve conter a resposta dada pelo usuário e o id da pergunta.
    """
    print "Alternativa selecionada: ", request.POST("alternativa")
    print "Id da pergunta: ", request.POST("perguntaId")
    return HttpResponse("Hmmm...")


    
    
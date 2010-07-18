# -*- coding: utf-8 -*-
from osindicados.jogo.models import Tema, Pergunta
from osindicados.jogo.partidaconfs import *
from django.shortcuts import render_to_response

def index(request):
    temas = Tema.objects.all()
    perguntas = Pergunta.objects.all()

    # calcula quantas perguntas foram cadastradas em cada tema
    list_tema_qntd = [(tema, len(Pergunta.objects.filter(idAssunto__exact=tema.id))) for tema in temas]

    return render_to_response('jogo/index.html', {'list_tema_qntd': list_tema_qntd, 'perguntas': perguntas})

def partida(request):
    return render_to_response('jogo/partida.html', {'confs': request.session['confs']})

def config(request):
    dificuldade = 2
    temas = ['Cinema', 'Musica']
    conf = Partidaconfs(dificuldade, temas)
    request.session['confs'] = conf
    return render_to_response('jogo/config.html')


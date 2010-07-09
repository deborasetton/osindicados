# -*- coding: utf-8 -*-
from osindicados.jogo.models import Tema, Pergunta
from django.shortcuts import render_to_response

def index(request):
    temas = Tema.objects.all()
    perguntas = Pergunta.objects.all()
    return render_to_response('jogo/index.html', {'temas': temas, 'perguntas': perguntas})


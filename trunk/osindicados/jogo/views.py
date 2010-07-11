# -*- coding: utf-8 -*-
from osindicados.jogo.models import Tema, Pergunta
from django.shortcuts import render_to_response

def index(request):
    temas = Tema.objects.all()
    perguntas = Pergunta.objects.all()

    # calcula quantas perguntas foram cadastradas em cada tema
    list_tema_qntd = [(tema, len(Pergunta.objects.filter(idAssunto__exact=tema.id))) for tema in temas]

    return render_to_response('jogo/index.html', {'list_tema_qntd': list_tema_qntd, 'perguntas': perguntas})


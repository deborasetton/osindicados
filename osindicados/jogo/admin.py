# -*- coding: utf-8 -*-
from django.contrib import admin
from osindicados.jogo.models import Pergunta
#from osindicados.jogo.models import Tema
#from osindicados.jogo.models import Placar

#admin.site.register(Pergunta)
#admin.site.register(Tema)
#admin.site.register(Placar)

class PerguntaAdmin(admin.ModelAdmin):
    #cadastro
    fieldsets = [
        (None, {'fields': ['enunciado'], 'classes': []}),
        ('Alternativa Correta', {'fields': ['altCorreta']}),
        ('Alternativas Incorretas', {'fields': ['altIncorreta1', 'altIncorreta2', 'altIncorreta3', 'altIncorreta4']}),
        (None,{'fields': ['idAssunto', 'dificuldade']}),
    ]
    #lista
    search_fields = ['enunciado']
    list_display = ('enunciado', 'idAssunto', 'dificuldade')
    list_filter = ('idAssunto', 'dificuldade')
    list_per_page = 50

admin.site.register(Pergunta, PerguntaAdmin)
